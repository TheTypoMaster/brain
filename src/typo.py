# -*- coding: utf-8 -*-
import requests, json, time, os, fileinput, sys, mimetypes, tempfile
from bs4 import BeautifulSoup
from binaryornot.check import is_binary

def main():
    words_file = open('words/words.txt', 'r')
    words = words_file.read().split('\n')
    words_file.close()

    word_results = []

    for line in words:
        try:
            if line == "":
                continue

            split_line = line.split(' - ', 1)

            correct = split_line[0].strip();
            wrong_words = split_line[1].split(',')

            for wrong in wrong_words:
                word_results.append((wrong.strip(), correct))
        except:
            print "Failed to parse line: %s" % line
            pass

    for wrong_word, correct_word in word_results:
        print "Scraping code search for word: %s" % wrong_word

        scraped_info = scrape_code_search(wrong_word)

        scraped_info_text = BeautifulSoup(scraped_info.text, "lxml")
        scraped_links = list(set(scraped_info_text.find_all('a')))

        repos_file = open('repos/repos.txt', 'w')

        for scraped_link in scraped_links:
            if "/" in scraped_link['href']:
                if "/" in scraped_link.get_text():
                    repos_file.write("%s\n" % scraped_link.get_text())
                    print "Added %s to file" % scraped_link.get_text()

        sorted_repos_file = os.popen("sort repos/repos.txt | uniq").read()
        repos_file.truncate()
        repos_file.write(sorted_repos_file)

        repos_file.close()

        print "Successfully scraped code search for word: %s" % wrong_word

        with open('repos/repos.txt', 'r') as repos_file_read:
            repos = repos_file_read.read().split('\n')
            for repo in repos:
                project_forked = False
                body = """
    Hi! I'm a bot that checks GitHub for spelling mistakes, and I found one in your repository. When it
    should be '%s', you typed '%s'. I created this pull request to fix it!

    If you think there is anything wrong with this pull request or just have a question, be kind to mail me 
    at thetypomaster@hotmail.com (professional email, huh?). I’ll try to address the problem as soon as
    I’m aware of it.

    If you decide to close this pull request, please specify why before doing so.

    With kind regards,
    TheTypoMaster
                """ % (correct_word, wrong_word)

                repo_name = repo.split('/', 1)[1]

                credentials_file = open('credentials.txt', 'r')
                username, password = credentials_file.read().split('\n')
                credentials_file.close()

                create_fork(repo, username, password)
                print "Created fork: %s" % repo

                while True:
                    forked_project = requests.get("https://github.com/TheTypoMaster/%s" % repo_name)
                    if 'This repository is empty' in forked_project.text:
                        print "Large project; sleeping a little bit!"
                        time.sleep(1)
                    else:
                        break;

                os.system("git clone https://github.com/TheTypoMaster/%s.git" % repo_name)
                print "Successfully cloned directory: %s" % repo_name

                for dirpath, dirnames, filenames in os.walk(repo_name):
                    for name in filenames:
                        path = os.path.join(dirpath, name)
                        mimetype_name = mimetypes.guess_type(path)[0]

                        try:
                            if is_binary(path):
                                print "File '%s' ignored, not a text file (%s)" % (path, mimetype_name)
                            else:
                                with open(path, 'r+w') as filepath:
                                    filecontent = filepath.read()
                                    
                                    if wrong_word in filecontent:
                                        print "Found '%s' in path: %s" % (wrong_word, path)

                                        filecontent = filecontent.replace(wrong_word, correct_word)

                                        filepath.truncate(0)
                                        filepath.seek(0)
                                        filepath.write(filecontent)
                                    else:
                                        print "Could not find '%s' in path: %s" % (wrong_word, path)
                        except IOError:
                            print "Could not find file: '%s'" % path 
                    if '.git' in dirnames:
                        dirnames.remove('.git')

                os.chdir(repo_name)

                os.system("git add .")
                os.system("git commit -m \"Fix typo '%s' \"" % wrong_word)
                os.system("git push -u https://github.com/TheTypoMaster/%s.git master" % repo_name)

                os.chdir('../')

                print "Pushed changes"

                create_pull_request(repo, "Fix typo '%s'" % wrong_word, body, username, password)

                print "Created pull request for project '%s'" % repo_name

                cleanup(repo_name)

                print "Deleted project and emptied trash"

                with open('repos/repos.txt', 'r') as fin:
                    data = fin.read().splitlines(True)

                with open('repos/repos.txt', 'w') as fout:
                    fout.writelines(data[1:])

                print "Removed first line from file"

                print "Finished!"

                time.sleep(1)

def create_fork(repo, username, password):
    requests.post('https://api.github.com/repos/%s/forks' % repo, auth=(username, password))

def create_pull_request(repo, title, body, username, password):
    payload = {'title': title, 'body': body, 'head': 'TheTypoMaster:master', 'base': 'master'}
    requests.post("https://api.github.com/repos/%s/pulls" % repo, json=payload, auth=(username, password))

def scrape_code_search(word):
    return requests.get("https://github.com/search?o=desc&p=1&q=%s&ref=searchresults&s=indexed&type=Code&utf8=✓" % word)

def cleanup(repo_name):
    os.system("rm -rf %s" % repo_name)
    os.system("rm -rf ~/.Trash/*") # Will only work on OS X

if __name__ == '__main__':
    main()
