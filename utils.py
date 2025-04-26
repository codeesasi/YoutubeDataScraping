import subprocess

def check_docker_installed():
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True, text=True)
        print("✅ Docker is installed.")
    except subprocess.CalledProcessError:
        print("❌ Docker is not installed. Please install Docker and try again.")
        exit(1)

def pull_images():
    try:
        print("📥 Pulling Redis image...")
        subprocess.run(["docker", "pull", "redis"], check=True)
        print("✅ Redis image pulled.")

    except subprocess.CalledProcessError as e:
        print("❌ Failed to pull one of the images:", e)
        exit(1)

def run_redis_container():
    try:
        print("🚀 Running Redis container...")
        subprocess.run([
            "docker", "run", "-d",
            "--name", "redis_server",
            "-p", "6379:6379",
            "redis"
        ], check=True)
        print("✅ Redis is running on port 6379.")
    except subprocess.CalledProcessError as e:
        print("❌ Failed to run Redis container:", e)

if __name__ == "__main__":
    check_docker_installed()
    pull_images()
    run_redis_container()