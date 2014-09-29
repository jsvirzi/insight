import subprocess

url = 'http://arxiv.org/list/hep-th/pastweek?skip=0&show=25'
url = 'http://jsvirzi.dyndns.org/index.html'

output = subprocess.Popen(['wget', url, '-O', '-', '-o', '/dev/null'], stdout = subprocess.PIPE, stderr = subprocess.STDOUT).communicate()[0]

i = 0
lines = output.split('\n')
for line in lines:
    i = i + 1
    print 'line(%d) = [%s]' % (i, line)
