import requests
import re
import json
from tqdm import tqdm


bads = ["jpg", "svg", "https", "ogg", "cite_note", "JPG", "png", "Portal"]


def special_match(strg, search=re.compile(r'[^a-zA-ZąćęłńóśźżĄĘŁŃÓŚŹŻ]').search):
    return not bool(search(strg))


def read_wiki_links(url, filename=None, folder_name="Firsts"):
    req = requests.get(url, 'html.parser')
    new_text = re.search('</head>(.*?)<h2>Menu nawigacyjne</h2>', req.text.replace("\n", ""))
    new_text = new_text.group(0)
    # print(new_text)
    a = re.findall('href=\"(.*?)\">', new_text)
    aa = []
    for patt in a:
        b = [re.findall("^(.*?)\" (title|class)", patt), re.findall("title=\"(.*)", patt)]
        aa.append(b)

    verbs = {}
    just_links = []
    for verb in aa:
        try:
            link = verb[0][0][0]
            bad_in = False
            for bad in bads:
                if bad in link:
                    bad_in = True
            if "/wiki/" in link and not bad_in and " " not in verb[1][0] and ":" not in verb[1][0] and special_match(verb[1][0]):
                verbs.update({verb[1][0]: link})
                just_links.append(link)
        except:
            pass

    # bad_links = []
    # for link in a:
    #     for bad in bads:
    #         if bad in link:
    #             bad_links.append(link)
    #             continue
    #
    #     if "/wiki/" not in link:
    #         bad_links.append(link)
    # bad_links = list(set(bad_links))
    # for bad_link in bad_links:
    #     a.remove(bad_link)

    just_links = "\n".join(just_links)

    if filename is not None:
        # with open("Files/" + filename + ".txt", 'w', encoding="utf-8") as f:
        #     f.write(just_links)
        #     f.close()
        to_save = {"verb": filename.replace("https://pl.wikipedia.org/wiki/", ""), "connections": verbs}
        with open("Files/" + folder_name + "/" + filename.replace("/", "_") + ".json", 'w', encoding="utf-8") as f:
            json.dump(to_save, f, indent=6)
            f.close()
    return verbs


def prepare_base():
    words = None
    try:
        with open("Files/ready.json", 'r', encoding="utf-8") as f:
            words = json.load(f)
            f.close()
    except FileNotFoundError:
        words = []
    return words


def read_words_recursive_until(read_words, new_verbs, current, max):
    for verb in new_verbs:
        if verb not in read_words:
            verbs = read_wiki_links(f'https://pl.wikipedia.org{new_verbs[verb]}', verb, "Connections")
            read_words.append(verb)
            if current < max:
                read_words_recursive_until(read_words, verbs, current+1, max)


all_words = prepare_base()

with open('Words.txt', 'r', encoding="utf-8") as f:
    lines = f.readlines()
words_pairs = lines
for pair in tqdm(words_pairs, desc="słowa z gry"):
    new_pair = pair.split("/")
    for word in new_pair:
        word = word.replace("\n", "")
        new_url = 'https://pl.wikipedia.org/wiki/' + word
        file_output_name = word
        new_verbs = read_wiki_links(new_url, file_output_name)
        read_words_recursive_until(all_words, new_verbs, 0, 3)

        with open("Files/ready.json", 'w', encoding="utf-8") as f:
            json.dump(all_words, f, indent=6)
            f.close()


# for verb in tqdm(new_verbs):
#     if verb not in all_words:
#         read_wiki_links(f'https://pl.wikipedia.org{new_verbs[verb]}', "Connections/"+verb)
#         all_words.append(verb)



