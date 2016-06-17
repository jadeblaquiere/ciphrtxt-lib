# Copyright (c) 2016, Joseph deBlaquiere <jadeblaquiere@yahoo.com>
# All rights reserved
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of ecpy nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from Crypto.Random import random

from ciphrtxt.keys import PublicKey, PrivateKey
from ciphrtxt.message import Message, MessageHeader

pkey = []
Pkey = []

print('creating alice keys')
alice = PrivateKey()
alice.randomize(4)
aliceP = PublicKey.deserialize(alice.serialize_pubkey())
print('creating bob keys')
bob = PrivateKey()
bob.randomize(4)
bobP = PublicKey.deserialize(bob.serialize_pubkey())
print('keys complete')

mtxt = 'the quick brown fox jumped over the lazy dog'
msg1 = Message.encode(mtxt, bobP, alice)
print('message1 = ' + msg1.serialize())
msg1a = Message.deserialize(msg1.serialize())
print('message1a = ' + msg1a.serialize())
if msg1a.decode(bob):
    print('decoded:', msg1a.ptxt)
msg2 = Message.encode_impersonate(mtxt, aliceP, bob)
print('message2 = ' + msg2.serialize())
msg2a = Message.deserialize(msg2.serialize())
print('message2a = ' + msg1a.serialize())
if msg2a.decode(bob):
    print('decoded:', msg1a.ptxt)

for i in range(0,1000):
    a = PrivateKey()
    a.randomize(random.randint(0,8))
    b = PublicKey.deserialize(a.serialize_pubkey())
    pkey.append(a)
    Pkey.append(b)

for i in range(0,1000):
    ztxt = ''
    for j in range(1,random.randint(2,10)):
        ztxt += mtxt
    f = random.randint(0,1000)
    t = random.randint(0,1000)
    m = Message.encode(ztxt, Pkey[t], pkey[f])
    ms = m.serialize()
    print('msg ' + str(i) + ' = ' + ms)
    md = Message.deserialize(ms)
    assert md.decode(pkey[t])
    print('mtxt = ' + md.ptxt)
    for j in range(0,1000):
        if j != t:
            assert not md.decode(pkey[j])