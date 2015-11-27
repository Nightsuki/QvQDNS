#!/usr/bin/env python
import socket
import argparse
import os
import re
from database import DNSLogs, DomainLogs, User

__author__ = 'Nightsuki'


# DNSQuery class from http://code.activestate.com/recipes/491264-mini-fake-dns-server/
class DNSQuery:
    def __init__(self, data):
        self.data = data
        self.dominio = ''

        tipo = (ord(data[2]) >> 3) & 15  # Opcode bits
        if tipo == 0:  # Standard query
            ini = 12
            lon = ord(data[ini])
            while lon != 0:
                self.dominio += data[ini + 1:ini + lon + 1] + '.'
                ini += lon + 1
                lon = ord(data[ini])

    def respuesta(self, ip):
        packet = ''
        if self.dominio:
            packet += self.data[:2] + "\x81\x80"
            packet += self.data[4:6] + self.data[4:6] + '\x00\x00\x00\x00'  # Questions and Answers Counts
            packet += self.data[12:]  # Original Domain Name Question
            packet += '\xc0\x0c'  # Pointer to domain name
            packet += '\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'  # Response type, ttl and resource data length -> 4 bytes
            packet += str.join('', map(lambda x: chr(int(x)), ip.split('.')))  # 4bytes of IP
        return packet


def domain_to_ip(domain):
    dnsserver = "8.8.8.8"
    seqid = os.urandom(2)
    host = ''.join(chr(len(x)) + x for x in domain.split('.'))
    data = '%s\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00%s\x00\x00\x01\x00\x01' % (seqid, host)
    sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
    sock.settimeout(None)
    sock.sendto(data, (dnsserver, 53))
    data = sock.recv(512)
    assert isinstance(data, basestring)
    iplist = ['.'.join(str(ord(x)) for x in s) for s in re.findall('\xc0.\x00\x01\x00\x01.{6}(.{4})', data) if
              all(ord(x) <= 255 for x in s)]
    return iplist


def start_qvq(domain, ip):
    domain = "%s." % domain
    qvqdns = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    qvqdns.bind(('', 53))
    try:
        print ("QvQDNS is listening on 0.0.0.0:53\n")
        while 1:
            data, addr = qvqdns.recvfrom(1024)
            try:
                p = DNSQuery(data)
            except:
                p = None
                pass
            if p and p.dominio.endswith(domain):
                qvqdns.sendto(p.respuesta(ip), addr)
                print("%s------%s" % (p.dominio[:-1], addr[0]))
                user = User.select().where(User.domain == p.dominio.split(domain)[0].split(".")[-1]).first()
                if user:
                    domain_query = DomainLogs.select().where(DomainLogs.domain == p.dominio[:-1]).first()
                    if domain_query:
                        domain_query = DomainLogs()
                        domain_query.user_id = user.id
                        domain_query.domain = p.dominio[:-1]
                        domain_query.save()
                    log = DNSLogs()
                    log.ip = addr[0]
                    log.user_id = user.id
                    log.domain_id = domain_query.id
                    log.save()
                    log = DNSLogs()
                    log.ip = addr[0]
                    log.user_id = user.id
                    log.domain_id = domain_query.id
                    log.save()
            else:
                print("%s------%s" % (p.dominio[:-1], addr[0]))
                try:
                    result = domain_to_ip(p.dominio[:-1])
                    qvqdns.sendto(p.respuesta(result[0]), addr)
                except:
                    pass
            del p
    except KeyboardInterrupt:
        qvqdns.close()
        print ("QvQDNS is closed!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", dest="domain", type=str, default="qvq.io", help="the domain you wanna monitor on")
    parser.add_argument("-i", dest="ip", type=str, default="103.238.224.61", help="the ip you wanna return")
    args = parser.parse_args()
    start_qvq(args.domain, args.ip)
