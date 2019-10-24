psHandle = os.popen("ps ax")
for psLine in psHandle.readlines():
    if "rclone mount" in psLine:
        print("Unmounting content repository...")
        os.system("kill " + psLine.split()[0])
psHandle.close()
