import datetime
import re

from SSHLogJournal import SSHLogJournal
from utils import MessageType


class SSHUser:
    def __init__(self, username: str, last_login_date: datetime.datetime | None):
        self.username = username
        self.last_login_date = last_login_date

    def __repr__(self):
        return f"{self.__class__.__name__}(username={self.username}, last_login_date={self.last_login_date})"

    def validate(self):
        pattern = r'^[a-z_][a-z0-9_-]{0,31}$'
        return re.match(pattern, self.username) is not None


if __name__ == '__main__':
    journal = SSHLogJournal()
    journal.append("Dec 10 06:55:46 LabSZ sshd[24200]: reverse mapping checking getaddrinfo for ns.marryaldkfaczcz.com [173.234.31.186] failed - POSSIBLE BREAK-IN ATTEMPT!")
    journal.append("Dec 10 06:55:46 LabSZ sshd[24200]: Invalid user webmaster from 173.234.31.186")
    journal.append("Dec 10 06:55:46 LabSZ sshd[24200]: input_userauth_request: invalid user webmaster [preauth]")
    journal.append("Dec 10 06:55:46 LabSZ sshd[24200]: pam_unix(sshd:auth): check pass; user unknown")
    journal.append("Dec 10 06:55:46 LabSZ sshd[24200]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=173.234.31.186")
    journal.append("Dec 10 06:55:48 LabSZ sshd[24200]: Failed password for invalid user webmaster from 173.234.31.186 port 38926 ssh2")
    journal.append("Dec 10 06:55:48 LabSZ sshd[24200]: Connection closed by 173.234.31.186 [preauth]")
    journal.append("Dec 10 07:02:47 LabSZ sshd[24203]: Connection closed by 212.47.254.145 [preauth]")
    journal.append("Dec 10 07:07:38 LabSZ sshd[24206]: Invalid user test9 from 52.80.34.196")
    journal.append("Dec 10 07:07:38 LabSZ sshd[24206]: input_userauth_request: invalid user test9 [preauth]")
    journal.append("Dec 10 07:07:38 LabSZ sshd[24206]: pam_unix(sshd:auth): check pass; user unknown")
    journal.append("Dec 10 07:07:38 LabSZ sshd[24206]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=ec2-52-80-34-196.cn-north-1.compute.amazonaws.com.cn")

    print("length of list: ", len(journal), "\n")
    print("slice list: \n", journal[1:3], "\n")
    print("list with given ipv4:\n", journal['173.234.31.186'], "\n")

    users = [SSHUser("webmaster", None), SSHUser("test9", None)]
    log_entries = journal.get_logs_by_type(MessageType.INVALID_PASSWORD)

    users_and_logs = users + log_entries

    print("users_and_logs:")
    for item in users_and_logs:
        print(item)
        if not item.validate():
            print(f"Invalid item: {item}")
            break
