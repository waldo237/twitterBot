from os import walk, path, rename


def find_photo():
    for (dirpath, dirnames, fnames) in walk('./photos'):
        for f in fnames:
            p = path.join("photos", f)
            if not '_done' in f:
                fn = p.split('.')
                new_name =  fn[0]+'_done.' + fn[1]
                rename(p, new_name)
                return new_name
            else:
                continue



