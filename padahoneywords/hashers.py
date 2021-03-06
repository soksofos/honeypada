
from pickle import dumps, loads
from ast import literal_eval
from base64 import b64encode
from random import shuffle
from xmlrpc.client import ServerProxy
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.utils.crypto import get_random_string, pbkdf2
from .honeywordsganaration import gen
from .models import Sweetwords

class HoneywordHasher(PBKDF2PasswordHasher):
    """Honeyword Hasher
    Subclass of django.contrib.auth.hashers.PBKDF2PasswordHasher
    """
    #  settings
    DEBUG = getattr(settings, 'DEBUG', None)
    HONEYWORDS_COUNT = getattr(settings, 'HONEYWORDS_COUNT', 19)
    try:
        HONEYCHECKER_URI = getattr(settings, 'HONEYCHECKER_URI')
    except AttributeError:
        raise ImproperlyConfigured(
            "Add `HONEYCHECKER_URI = 'http(s)://<url>:<port>'` to Django settings"
            )

    algorithm = "honeyword_base9_tweak3_pbdkf2_sha256"
    honeychecker = ServerProxy(HONEYCHECKER_URI)

    def hash(self, password, salt, iterations):
        hash = pbkdf2(password, salt, iterations, digest=self.digest)
        print('try to und encode')
        print(b64encode(hash).decode('ascii').strip())
        return b64encode(hash).decode('ascii').strip()

    def salt(self):
        salt = get_random_string(20)
        while Sweetwords.objects.filter(salt=salt).exists():
            salt = get_random_string(20)
        print("this is salt")
        print(salt)
        return salt

    def verify(self, password, encoded):
        algorithm, iterations, salt, dummy = encoded.split('$', 3)
        # safely convert bytestring representation to bytes
        sweetwords = literal_eval(Sweetwords.objects.get(salt=salt).sweetwords)
        hashes = loads(sweetwords)
        hash = self.hash(password, salt, int(iterations))
        if hash in hashes:
            try:
                is_valid = self.honeychecker.check_index(salt, hashes.index(hash))
                # TODO implement logging
                #if not is_valid: print("BADWORD TRIGGERED")
                return "CORRECT" if is_valid else "BADWORD"
            # TODO implement honeychecker failure default settings
            except ConnectionRefusedError:
                # Allow login if Honeychecker is down
                return "CORRECT"
        return False

    def encode(self, password, salt, iterations=PBKDF2PasswordHasher.iterations):
        sweetwords = [password]
        sweetwords.extend(gen(password, self.HONEYWORDS_COUNT, []))
        # TODO implement honeywordtweak
        #for i in range(<bases+1>):
        #    sweetwords.extend(honeywordtweak.tweak(passwords[i], <tweaks>))
        # TODO move test password into test suite instead
        if self.DEBUG:
            print("WARNING: In DEBUG mode, 'test' is added as a honeyword.")
            sweetwords.extend(['pada123'])
        shuffle(sweetwords)
        hashes = []
        for swd in sweetwords:
            hashes.append(self.hash(swd, salt, iterations))
        # TODO implement honeychecker failure response for saving index
        self.honeychecker.update_index(salt, sweetwords.index(password))
        h = Sweetwords(salt=salt, sweetwords=dumps(hashes))
        h.save()
        print('encode')
        print(f"{self.algorithm}${iterations}${salt}${hashes[0]}")
        return f"{self.algorithm}${iterations}${salt}${hashes[0]}"
