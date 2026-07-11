import datetime
import os
import re
import requests
from lxml import etree

BIRTHDAY = datetime.date(2003, 9, 7)
USER_NAME = os.environ.get("USER_NAME", "adityaverma9777")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN", "")
HEADERS = {"Authorization": f"token {ACCESS_TOKEN}"} if ACCESS_TOKEN else {}

HERE = os.path.dirname(os.path.abspath(__file__))
DARK_SVG = os.path.join(HERE, "dark_mode.svg")
LIGHT_SVG = os.path.join(HERE, "light_mode.svg")


# Uptime removed


def gh_query(query, variables=None):
    r = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": variables or {}},
        headers=HEADERS,
        timeout=30,
    )
    r.raise_for_status()
    return r.json()


def get_stats():
    rest_url = f"https://api.github.com/users/{USER_NAME}"
    try:
        r = requests.get(rest_url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        d = r.json()
        repos = d.get("public_repos", 0)
        followers = d.get("followers", 0)
    except Exception as e:
        print(f"REST fetch failed: {e}")
        return None, None, None, None, None
    if not ACCESS_TOKEN:
        return repos, None, None, followers, None
    query = """
    query($login: String!) {
      user(login: $login) {
        repositoriesContributedTo(first: 1) { totalCount }
        starredRepositories { totalCount }
        contributionsCollection {
          totalCommitContributions
          restrictedContributionsCount
        }
      }
    }"""
    try:
        data = gh_query(query, {"login": USER_NAME})["data"]["user"]
        contributed = data["repositoriesContributedTo"]["totalCount"]
        stars = data["starredRepositories"]["totalCount"]
        cc = data["contributionsCollection"]
        commits = cc["totalCommitContributions"] + cc["restrictedContributionsCount"]
        return repos, contributed, stars, followers, commits
    except Exception as e:
        print(f"GraphQL fetch failed: {e}")
        return repos, None, None, followers, None


def pad_dots(current_dots, old_val, new_val):
    diff = len(str(new_val)) - len(str(old_val))
    if diff > 0:
        return current_dots[:-diff] if len(current_dots) > diff else "."
    elif diff < 0:
        return current_dots + "." * (-diff)
    return current_dots


def update_svg(path, age_str, repos, contributed, stars, followers, commits):
    parser = etree.XMLParser(remove_blank_text=False)
    tree = etree.parse(path, parser)
    root = tree.getroot()

    def find(id_val):
        return root.find(f'.//*[@id="{id_val}"]')

    age_el = find("age_data")
    if age_el is not None:
        dots_el = find("age_data_dots")
        if dots_el is not None and age_el.text:
            dots_el.text = pad_dots(dots_el.text or "", age_el.text or "", age_str)
        age_el.text = age_str

    def set_stat(id_name, dots_id, value):
        el = find(id_name)
        if el is not None and value is not None:
            dots_el = find(dots_id)
            if dots_el is not None and el.text:
                dots_el.text = pad_dots(dots_el.text or "", el.text or "", str(value))
            el.text = str(value)

    set_stat("repo_data", "repo_data_dots", repos)
    set_stat("contrib_data", "repo_data_dots", contributed)
    set_stat("star_data", "star_data_dots", stars)
    set_stat("follower_data", "follower_data_dots", followers)
    set_stat("commit_data", "commit_data_dots", commits)

    tree.write(path, xml_declaration=True, encoding="UTF-8", pretty_print=False)
    print(f"updated {path}")


if __name__ == "__main__":
    repos, contributed, stars, followers, commits = get_stats()
    print(f"Repos: {repos}, Contributed: {contributed}, Stars: {stars}, Followers: {followers}, Commits: {commits}")
    for svg_path in [DARK_SVG, LIGHT_SVG]:
        update_svg(svg_path, "", repos, contributed, stars, followers, commits)
