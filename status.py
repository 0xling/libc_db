__author__ = 'ling'

def status():
    f = open('./symbol_db', 'rb')
    ubuntu = 0
    debian = 0
    fedora = 0
    arch = 0
    local = 0
    unknown = 0
    total = 0
    for line in f:
        if line.startswith('#'):
            continue
        name = line.split(' ')[1].strip()
        total += 1
        if 'ubuntu' in name:
            ubuntu +=1
        elif 'debian' in name:
            debian += 1
        elif 'arch' in name:
            arch += 1
        elif 'fedora' in name:
            fedora += 1
        elif 'local' in line:
            local += 1
        else:
            unknown += 1
    f.close()
    print 'status'
    print ' ubuntu:%d' %ubuntu
    print ' debian:%d' %debian
    print ' fedora:%d' %fedora
    print ' arch:%d' %arch
    print ' local:%d' %local
    print ' unknown:%d' %unknown
    print 'total:%d' %total
