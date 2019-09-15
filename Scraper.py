import re

from LinkObject import LinkObject
import time

link_dict = {}
max_result_count = 50
verbose = False


def format_url(found_url, root_url):
    # remove ? and # extensions or cases where url is just '/'
    found_url = re.sub(r'(#.*)|(\?.*)|(^/$)', '', found_url)

    # remove mailto links
    if re.search(r'^mailto', found_url):
        found_url = ""

    if len(found_url) > 0:

        # if url is subdirectory link - needs work
        sub_match = re.match(r'(^http)|(^www.)', found_url)
        if not sub_match:
            found_url = root_url + found_url

        # add forward slash to end of url if ending in .com or a path that doesn't end in a slash
        # (.com)$ finds strings ending in .com
        # ((?<=/)[^.]+[^/]$) finds strings not ending in a filename extension
        if re.search(r'(.com)$|((?<=/)[^.]+[^/]$)', found_url):
            found_url += "/"

        # replace any double forward slashes not following http: or https:
        found_url = re.sub(r'(?<=[^:])//', "/", found_url)

    return found_url


def scrape(root_url):
    link_object = link_dict[root_url]
    # search

    # if not first run, download page
    if not link_object.hasHtml:
        link_object.get_response()

    # if url had valid response, search page for links
    if link_object.valid:
        # search

        # (?:<a ).*href=[\"|'](.+?(?=[\'|\"])) captures it in capture group 1

        matches_a_group = re.findall(r'(?:<a ).*href=[\"|\'](.+?(?=[\'|\"]))', link_object.html)
        matches_href = []

        # add all matches to dictionary or adjust their find count
        for match in matches_a_group:
            if len(link_dict) < max_result_count:

                found_url = format_url(match, root_url)

                if len(found_url) > 0:

                    matches_href.append(found_url)

                    if found_url in link_dict.keys():
                        pass
                        # link_dict[found_url].increase_count()
                    else:
                        new_link_object = LinkObject(found_url)
                        link_dict[found_url] = new_link_object
            else:
                return
        link_object.set_scraped(True)

        # depth first scrape
        if len(link_dict) < max_result_count:
            for match in matches_href:
                if not link_dict[match].scraped:
                    scrape(match)


def finish():
    for key, value in link_dict.items():
        print(key)
        global verbose
        if verbose:
            print(value)
            print()


def first_url(url):
    link_object = LinkObject(url)
    link_dict[url] = link_object

    link_object.get_response()

    if link_object.valid:
        scrape(url)
        finish()
    else:
        print("Unable to scrape due to the following error with the provided link:\n" + link_object.ErrorReason)


def run(url):
    start = time.time()
    first_url(url)
    end = time.time()
    print("Running time: " + (end - start).__str__())


def run(url, result_count):
    global max_result_count
    max_result_count = result_count
    start = time.time()
    first_url(url)
    end = time.time()
    print("Running time: " + (end - start).__str__())


def run(url, result_count, verbose_flag):
    global max_result_count
    max_result_count = result_count
    global verbose
    verbose = verbose_flag
    start = time.time()
    first_url(url)
    end = time.time()
    print("Running time: " + (end - start).__str__())


class Scaper:
    pass
