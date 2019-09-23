import re

from LinkObject import LinkObject
import time

# The dictionary containing all unique found links and their LinkObject
link_dict = {}

# The number of unique links that will be searched for
max_result_count = 100

# Flag used to determine whether whole LinkObject should be printed
verbose = False

# Flag to determine whether ? and # links should be filtered
just_urls = True

# list used for breadth first to keep track of found items
link_object_list = []


# Function used to format a found url
# It takes the found url, and the URL of the page where it was found
# It removes ? and # extensions, deletes mailto links, concatenates reference urls with the parent url,
# adds a forward slash to the end of urls not ending in an extension, and replaces any double forward slashes
def format_url(found_url, parent_url):
    # Remove ? and # extensions
    if just_urls:
        found_url = re.sub(r'(#.*)|(\?.*)', '', found_url)

    # Remove mailto links or cases where url is just '/'
    if re.search(r'(^mailto)|(^/$)', found_url):
        found_url = ""

    # remove any slashes at the end of the url
    found_url = re.sub(r'/$', "", found_url)

    if len(found_url) > 0:

        # If url is subdirectory link concatenate with parent url
        sub_match = re.match(r'(^http)|(^www.)', found_url)
        root_url = ""

        if not sub_match:
            search = re.findall(r'^.+?(?<=[^:/])/', parent_url)
            if len(search) > 0:
                root_url = search[0]
            else:
                root_url = re.findall(r'^.+?(?<=[^/])$', parent_url)[0]
            found_url = root_url + "/" + found_url

        # Replace any double forward slashes not following http: or https:
        found_url = re.sub(r'(?<=[^:])//+', "/", found_url)

    return found_url


# recursive depth first scraping algorithm
def depth_first_scrape(root_url):
    link_object = link_dict[root_url]

    # if not first run, download page
    if not link_object.has_html:
        link_object.get_response()

    # if url had valid response, search page for links
    if link_object.valid:

        # search
        # (?<=<a ).+?(?<=href=['|\"])(.+?(?=['|\"])) working captures link in capture group 1
        matches_a_group = re.findall(r'(?<=<a ).+?(?<=href=[\'|\"])(.+?(?=[\'|\"]))', link_object.html)
        matches_href = []

        # add all matches to dictionary or adjust their find count
        for match in matches_a_group:
            if len(link_dict) < max_result_count:

                found_url = format_url(match, root_url)

                if len(found_url) > 0:

                    matches_href.append(found_url)

                    if found_url in link_dict.keys():
                        link_dict[found_url].increase_count()
                    else:
                        new_link_object = LinkObject(found_url)
                        link_dict[found_url] = new_link_object
            else:
                return
        link_object.set_scraped(True)

        # depth first scrape

        for match in matches_href:
            if not link_dict[match].scraped and len(link_dict) < max_result_count:
                depth_first_scrape(match)
    else:
        pass


# Function to print each item in the dictionary of found links
def finish():
    for key, value in link_dict.items():
        print(key)
        global verbose
        if verbose:
            print(value)
            print()


# clears any found results
def clear_results():
    link_dict.clear()
    link_object_list.clear()


# Function used to check whether the initial url provided is able to be visited
# adds link to link_dict
def first_url_check(url):
    link_object = LinkObject(url)
    link_dict[url] = link_object

    link_object.get_response()

    if link_object.valid:
        return True
    else:
        print("Unable to scrape due to the following error with the provided link:\n" + link_object.error_reason)
        return False


#breadth first scraping algorithm
def breadth_first_scrape(url):
    url = format_url(url, "")
    first_link_object = LinkObject(url)
    link_dict[url] = first_link_object
    link_object_list.append(first_link_object)

    # loop through enumerate of list to allow adding of links to search
    # using enumerate is poor for performance but required here
    for i, current_link_object in enumerate(link_object_list):
        if len(link_dict) < max_result_count:

            current_link_object.get_response()

            # if url had valid response, search page for links
            if current_link_object.valid:
                matches_a_group = re.findall(r'(?<=<a ).+?(?<=href=[\'|\"])(.+?(?=[\'|\"]))', current_link_object.html)

                # add all matches to dictionary or adjust their find count
                for match in matches_a_group:

                    if len(link_dict) < max_result_count:
                        found_url = format_url(match, current_link_object.url)

                        if len(found_url) > 0:

                            if found_url not in link_dict.keys():

                                new_link_object = LinkObject(found_url)
                                link_dict[found_url] = new_link_object
                                link_object_list.append(new_link_object)
                            else:
                                link_dict[found_url].increase_count()
                    else:
                        continue    # skip processing if reached count

            else:
                if len(link_dict) == 0:  # check if first link
                    print("Unable to scrape due to the following error with the provided link:\n" + current_link_object.error_reason)
                    break
        else:
            break


# Run the program using a depth first recursive search with the provided url
# Return the provided number of unique results
# verbose_flag used to set print detail level
# just_url_flag used to set whether search should filter # and ? extensions to urls
def run_depth_first(url, result_count, verbose_flag, just_url_flag):
    global max_result_count
    max_result_count = result_count
    global verbose
    verbose = verbose_flag
    global just_urls
    just_urls = just_url_flag

    start = time.time()

    url = format_url(url, "")

    if first_url_check(url):
        depth_first_scrape(url)
        finish()

    end = time.time()
    print("Running time: " + (end - start).__str__())


# Run the program using a breadth first search with the provided url
# Return the provided number of unique results
# verbose_flag used to set print detail level
# just_url_flag used to set whether search should filter # and ? extensions to urls
def run_breadth_first(url, result_count, verbose_flag, just_url_flag):
    global max_result_count
    max_result_count = result_count
    global verbose
    verbose = verbose_flag
    global just_urls
    just_urls = just_url_flag

    start = time.time()

    breadth_first_scrape(url)
    finish()

    end = time.time()
    print("Running time: " + (end - start).__str__())


# Runs depth first with default config
def run_default_df(url):
    run_depth_first(url, 100, False, True)


# Runs breadth first with default config
def run_default_bf(url):
    run_breadth_first(url, 100, False, True)


class Scaper:
    pass
