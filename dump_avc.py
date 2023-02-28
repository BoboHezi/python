#!/usr/bin/python
import re, sys, os

def main(argv):
    avc_log_path = argv[1] if len(argv) > 1 else 'avc.log'

    if not os.path.isfile(avc_log_path):
        print(f'{avc_log_path} is not a file')
        return

    print(f'read {avc_log_path}')
    pattern = 'avc:[ ]+denied[ ]+{([^}]+)}.*scontext=[^:]+:[^:]+:([^:]+):[\S]+ tcontext=[^:]+:[^:]+:([^:]+):[\S]+ tclass=([\S]+) permissive=1'
    avc_item = {}
    avc_log_file = open(avc_log_path, 'r')
    while True:
        line = avc_log_file.readline()
        if len(line) <= 0:
            break
        mth = re.search(pattern, line)
        if mth == None:
            continue
        permiss = mth.group(1).strip().split(' ')
        scontext = mth.group(2).strip()
        tcontext = mth.group(3).strip()
        tclass = mth.group(4).strip()
        key = f'allow {scontext} {tcontext}:{tclass}'

        if key not in avc_item:
            permissions = {x for x in permiss}
        else:
            permissions = avc_item[key]
            for perm in permiss:
                permissions.add(perm)

        avc_item[key] = permissions
    avc_log_file.close()

    if os.path.isfile(f'{avc_log_path}.te'):
        os.remove(f'{avc_log_path}.te')
    avc_content_file = open(f'{avc_log_path}.te', 'w')
    for k, v in avc_item.items():
        p = ' '.join([x for x in v])
        p = '{ %s };' % p
        avc_content_file.writelines(f'{k} {p}\n')
        print(f'{k} {p}')
    avc_content_file.close()

if __name__ == '__main__':
    main(sys.argv)
