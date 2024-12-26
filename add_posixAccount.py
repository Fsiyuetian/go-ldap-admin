#!/usr/bin/env python3
# coding=utf-8
# @Author: pingping.tu
# @Time  : 2024/12/25 17:45
# @Desc  : 配置定时任务可自动增加objectClass：posixAccount（依赖gidNumber、homeDirectory、uidNumber）

from ldap3 import Server, Connection, ALL, SUBTREE, ALL_ATTRIBUTES, MODIFY_ADD
import logging
import hashlib

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OpenLdap(object):
    def __init__(self):
        self._ip = '192.168.10.38'
        self._port = 389
        self._user = 'cn=admin,dc=xxxx,dc=com'
        self._passwd = 'xxxx'
        self.user_ou = 'ou=people'
        self.dn = 'dc=xxxx,dc=com'

    def conn(self):
        logging.info('Initializing LDAP connection...')
        server = Server(self._ip, self._port, get_info=ALL)
        conn = Connection(server, self._user, self._passwd, auto_bind=True)
        logging.info(f'Connection established: {conn}')
        return conn

    def search_user_all(self, lg):
        logging.info('Searching for all users...')
        search_base = f'{self.user_ou},{self.dn}'
        try:
            entry_list = lg.extend.standard.paged_search(
                search_base=search_base,
                search_filter='(objectClass=inetOrgPerson)',
                search_scope=SUBTREE,
                attributes=ALL_ATTRIBUTES,
                paged_size=5,
                generator=False
            )
            # logging.info(f'Search results: {entry_list}')
            logging.info(f'Search entry count: {len(entry_list)}')
            return entry_list
        except Exception as e:
            logging.error(f'Search error: {e}')
            raise

    def no_posixAccount_users(self, lg):
        logging.info('Searching for users without posixAccount...')
        entry_list = self.search_user_all(lg)
        users = []
        for entry in entry_list:
            if "posixAccount" not in entry['attributes']['objectClass']:
                uid = entry['attributes']['uid'][0]
                users.append(uid)
                logging.info(f'{uid} has no posixAccount')
        return users

    def generate_uid_number(self, uid):
        # 使用 SHA-256 哈希算法生成哈希值，并取前8个字符转换为整数
        hash_object = hashlib.sha256(uid.encode())
        hash_hex = hash_object.hexdigest()[:8]
        uid_number = int(hash_hex, 16) % (10 ** 9)  # 确保 uidNumber 在合理范围内
        return uid_number

    def add_attribute(self, lg):
        logging.info('Adding attributes...')
        users = self.no_posixAccount_users(lg)
        count_success = 0
        count_failed = 0
        for uid in users:
            if uid == 'RL0093':
                dn = f'uid={uid},{self.user_ou},{self.dn}'
                uid_number = self.generate_uid_number(uid)
                mod_attrs = {
                    'gidNumber': [(MODIFY_ADD, ['1'])],
                    'homeDirectory': [(MODIFY_ADD, [f'/home/users/{uid}'])],
                    'uidNumber': [(MODIFY_ADD, [str(uid_number)])],
                    'objectClass': [(MODIFY_ADD, ['posixAccount'])]
                }
                try:
                    lg.modify(dn, mod_attrs)
                    if lg.result['description'] == 'success':
                        logging.info(f'Successfully added attributes to {dn}')
                        count_success += 1
                    else:
                        logging.error(f'Failed to add attributes to {dn}: {lg.result}')
                        count_failed += 1
                except Exception as e:
                    logging.error(f'Error adding attributes to {dn}: {e}')
                    count_failed += 1
        print(f"Successfully count: {count_success}, Failed count: {count_failed}")
        return True


if __name__ == "__main__":
    ldap = OpenLdap()
    lg = ldap.conn()
    ad = ldap.add_attribute(lg)
    print(ad)















