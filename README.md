# TheTypoMaster's Brain

This code is what controls the behaviour of [@TheTypoMaster](https://github.com/thetypomaster), a bot which searches for a typo and finds the latest repositories with that typo. It fixes the typo/typos in the repository and submits a pull request.

Unlike [@thoppe](https://github.com/thoppe)'s [orthographic-pedant](https://github.com/thoppe/orthographic-pedant), this bot isn't searching through just the README file but all text files it can get its hands on.

## Word list
To search for the typos and check them, the TheTypoMaster is taking help from a text file with about ~4500 wrongly spelled words and the right spelled version of that. You can find it [here](words/words.txt).

## Credentials
To turn this project into your own (though it is quite dangerous), please create a credentials folder and put a credentials.txt file in that with the first and second lines like:

    username
    password

## A special thanks to
* [@holmstrom](https://github.com/holmstrom)
* [@thoppe](https://github.com/thoppe)
* [@maht0rz](https://github.com/maht0rz)
* [@sbrl](https://github.com/sbrl)

Without this people, this project probably would have been really bad and not even up on GitHub.

## But, like, why aren't you submitting any pull requests?
An automated pull request is forbidden on GitHub, and unless the user specified that their repository specifically accepts automated pull requests, you are on a dangerous road. My account has already been flagged, but thanks to the nice people working over at GitHub they unflagged it. **Please** use this bot with caution.

## TODO:
* Make everything a little prettier and extract some functionality in to its own functions.
* Extract the body of the pull request into its own file.
* Implement somewhat of a decent code distinguishment, if any.

## Super-duper-fun-mega-exciting stuff!! :D
This code is released under the [MIT License](LICENSE).