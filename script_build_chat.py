import builder
import os
import sys
import webbrowser

usage = "script_build_chat.py <number of msgs in chat>"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print usage
        sys.exit()
    builder.build(int(sys.argv[1]))
    print "Saved new bot_chat.html"
    webbrowser.open_new_tab('file://{0}'.format(os.path.realpath('bot_chat.html')))
else:
    print "don't import this"