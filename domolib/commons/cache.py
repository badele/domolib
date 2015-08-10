import os
import time
import json

class cache(object):
    def __init__(self, **kwargs):
        if 'rootcache' in kwargs:
            self.rootcache = kwargs['rootcache']
        else:
            self.rootcache = '/tmp/domolib'

        if 'cachefile' in kwargs:
            self.cachefile = kwargs['cachefile']
        else:
            self.cachefile = None


        # make rootcache directory
        if not os.path.exists(self.rootcache):
            os.makedirs(self.rootcache)


    def getcachedresults(self, cachefile=None,cachetime=1200):

        # Check the cachefile is set
        if not cachefile:
            if self.cachefile:
                cachefile = self.cachefile
            else:
                raise Exception("Please set cachefile in the cache class")

        filename = '%s/%s' % (self.rootcache, cachefile)
        if not os.path.exists(filename):
            # Cache not exists
            return None

        # Check if i use the cache results
        mtime = os.stat(filename).st_mtime
        now = time.time()
        if (now - mtime) > cachetime:
            # Cache is old
            return None

        # Use the cache file
        lines = open(filename).read()
        results = json.loads(lines)

        return results

    def setcacheresults(self,result, cachefile=None):

        # Check the cachefile is set
        if not cachefile:
            if self.cachefile:
                cachefile = self.cachefile
            else:
                raise Exception("Please set cachefile in the cache class")

        # Write result in the cachefile
        filename = '%s/%s' % (self.rootcache, cachefile)
        try:
            with open(filename, 'w') as f:
                jsontext = json.dumps(
                    result, sort_keys=True,
                    indent=4, separators=(',', ': ')
                )
                f.write(jsontext)
                f.close()
        except:
            os.remove(filename)
