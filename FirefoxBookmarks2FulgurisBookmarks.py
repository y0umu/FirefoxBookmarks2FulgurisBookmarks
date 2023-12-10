'''
Convert Firefox bookmarks to Fulguris bookmarks
'''
import json
import argparse

def format_pathname(pathname: str):
    '''
    replace
        / (forward slash)
        < (less than)
        > (greater than)
        : (colon - sometimes works, but is actually NTFS Alternate Data Streams)
        " (double quote)
        / (forward slash)
        \ (backslash)
        | (vertical bar or pipe)
        ? (question mark)
        * (asterisk)
    with . (a dot) in pathname
    '''
    if len(pathname) == 0:
        pathname = '➡️'   # emoji right arrow, code point: U+27A1 U+FE0F
    else:
        pathname.replace('/', '.')
        pathname.replace('<', '.')
        pathname.replace('>', '.')
        pathname.replace(':', '.')
        pathname.replace('"', '.')
        pathname.replace('/', '.')
        pathname.replace('\\', '.')
        pathname.replace('|', '.')
        pathname.replace('?', '.')
        pathname.replace('*', '.')
    return pathname

class Collection:
    def __init__(self):
        self.collection = {}  # the internal data that holds the bookmarks

    def from_firefox(self, ffjson: str):
        '''
        @param ffjson: path to a firefox backup json file
        '''
        with open(ffjson, 'r') as f:
            self.collection = json.load(f)
    
    def walk_collection(self):
        '''
        traverse the collection and print each node in self.collection
        in breadth first order

        yields a node each time
        '''
        queue = []
        # path_trace = []
        print(self.collection['title'])
        if 'children' in self.collection:
            queue.extend(self.collection['children'])
        while len(queue) > 0:
            this_node = queue.pop(0)
            # print(this_node['title'])
            if 'children' in this_node:
                queue.extend(this_node['children'])
            yield this_node

    def to_fulguris(self, fulguris_bookmark_file='save.txt', start_order=0):
        '''
        param fulguris_bookmark: path to save
        '''
        order = start_order
        foldername = ''
        with open(fulguris_bookmark_file, 'w+') as fw:
            for node in self.walk_collection():
                if node['typeCode'] == 1:  # a uri node
                    folder = 'Firefox import'
                    bookmark = {
                        'title': node['title'],
                        'url': node['uri'],
                        'folder': folder,
                        'order': order
                    }   # single line of one bookmark
                    order += 1
                    json.dump(bookmark, fw, ensure_ascii=False)
                    fw.write('\n')   #  write newline



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('firefox_bookmarks', help='Path to your Firefox JSON bookmarks')
    parser.add_argument('-o', '--output', default='FulgurisBookmarks_from_Firefox.txt', help='Filename to be written. Default: FulgurisBookmarks_from_Firefox.txt')
    parser.add_argument('--start-order', type=int, default=0, help='Start order of fulguris bookmark. Default: 0')
    args = parser.parse_args()
    bookmarks = Collection()
    bookmarks.from_firefox(args.firefox_bookmarks)
    bookmarks.to_fulguris(args.output, start_order=args.start_order)
    print(f'Written to {args.output}.')


if __name__ == '__main__':
    main()
