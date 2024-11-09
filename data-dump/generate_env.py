from random import SystemRandom
from string import ascii_uppercase, ascii_lowercase, digits
def password_of_length(length):
    return ''.join(SystemRandom().choice(ascii_uppercase + digits + ascii_lowercase) for _ in range(length))

keys = [
    "DB_ROOT_KEY",
    "AGENT_KEY",
    "ADMIN_KEY"
]

def main():
    env = []
    for key in keys:
        env.append(f"{key}={password_of_length(32)}")
    with open('.env', 'w') as f:
        f.write("\n".join(env))

if __name__ == '__main__':
    main()
