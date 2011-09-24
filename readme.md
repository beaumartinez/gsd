# GSD

GSD, short for Getting Shit Done™, toggles mapping a list of hosts to the loopback interface in the hosts file.

It's inspired by Vic Cherubni's [get-shit-done].

[get-shit-done]: http://github.com/leftnode/get-shit-done 

## Installation

It's one command. Run the [install script]:

[install script]: http://github.com/beaumartinez/gsd/blob/master/install.sh

    curl -s https://raw.github.com/beaumartinez/gsd/master/install.sh | bash

—And you're done!

## Usage

To start getting shit done:

    gsd start

To stop getting shit done:

    gsd stop

## Under the hood

GSD uses a special file, "the sites file", `~/.gsd-sites` with the domains to map, each separated by a space character. For example:

    twitter.com www.facebook.com

Or

    twitter.com
    www.facebook.com

These get written to the hosts file as:

    # GSD start
    127.0.0.1 twitter.com
    127.0.0.1 www.facebook.com
    # GSD end
