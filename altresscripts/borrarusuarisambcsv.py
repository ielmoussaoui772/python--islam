import subprocess

users_to_keep = ["root", "islam"]

def get_all_users():
    try:
        result = subprocess.check_output(["cut", "-d:", "-f1", "/etc/passwd"]).decode("utf-8").splitlines()
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error al obtener la lista de usuarios: {e}")
        return []

def delete_user(username):
    try:
        subprocess.run(["sudo", "deluser", "--remove-home", username], check=True)
        print(f"Usuario '{username}' eliminado con éxito.")
    except subprocess.CalledProcessError as e:
        print(f"Error al eliminar el usuario '{username}': {e}")

def main():
    all_users = get_all_users()

    for user in all_users:
        if user not in users_to_keep:
            try:
                uid = int(subprocess.check_output(["id", "-u", user]).decode("utf-8").strip())
                if uid >= 1000:
                    delete_user(user)
            except ValueError:
                print(f"Error al obtener el UID para el usuario '{user}'.")

if __name__ == "__main__":
    main()
