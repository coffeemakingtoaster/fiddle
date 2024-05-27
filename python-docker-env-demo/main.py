import os

def main():
    token = os.getenv("SECRET_TOKEN")
    if token:
        print(token)
    else:
        print("No token uwu")

if __name__ == "__main__":
    main()
