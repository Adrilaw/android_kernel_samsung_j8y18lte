import os
import subprocess
import sys
import shutil

# Function to check if the toolchain exists
def check_toolchain(toolchain_path):
    return os.path.exists(toolchain_path)

# Function to download the toolchain from GitHub
def download_toolchain(repo_url, toolchain_dir):
    try:
        print(f"[INFO] Toolchain not found. Cloning from {repo_url}...")
        subprocess.run(["git", "clone", repo_url, toolchain_dir], check=True)
        print("[SUCCESS] Toolchain downloaded successfully.")
    except subprocess.CalledProcessError:
        print("[ERROR] Failed to clone the toolchain. Please check your connection or the URL.")
        sys.exit(1)

# Function to set up environment variables
def setup_env_variables(toolchain_dir):
    print("[INFO] Setting up environment variables...")
    os.environ["ARCH"] = "arm64"
    os.environ["SUBARCH"] = "arm64"
    os.environ["CROSS_COMPILE"] = os.path.join(os.getcwd(), toolchain_dir, "bin/aarch64-linux-android-")

# Function to apply patches from the patches directory to the kernel directory
def apply_patches(patches_dir, kernel_dir):
    patch_files = [
        "add-cdrom-frozencow-3.18.patch",
        "add-HID-km-support-oneplus___msm8996-los_3.18.patch",
        "fix-rt2800-injection-3.18.patch"
    ]

    for patch_file in patch_files:
        full_patch_path = os.path.join(patches_dir, patch_file)
        
        if os.path.exists(full_patch_path):
            has_applied = input(f"[QUESTION] Have you already applied the patch {patch_file}? (yes/no): ").strip().lower()
            if has_applied == 'yes':
                print(f"[INFO] Skipping patch application as it is already applied: {patch_file}.")
            else:
                print(f"[INFO] Applying patch {patch_file} with patch -p1...")
                try:
                    with open(full_patch_path, 'r') as patch:
                        subprocess.run(["patch", "-p1"], cwd=kernel_dir, stdin=patch, check=True)
                    print(f"[SUCCESS] Patch applied successfully: {patch_file}.")
                except subprocess.CalledProcessError as e:
                    print(f"[ERROR] Failed to apply the patch: {patch_file}. Error: {e}")
                    sys.exit(1)
        else:
            print(f"[WARNING] Patch file {patch_file} does not exist in {patches_dir}. Continuing without applying the patch.")

# Function to configure the kernel and build
def configure_and_build_kernel(kernel_dir):
    try:
        print("[INFO] Running j8y18lte_defconfig...")
        subprocess.run(["make", "j8y18lte_defconfig"], cwd=kernel_dir, check=True)
        
        print("[INFO] Opening menuconfig for user modifications...")
        print("[INFO] Please refer to the NetHunter documentation on kernel configurations for guidance.")
        subprocess.run(["make", "menuconfig"], cwd=kernel_dir, check=True)
        
        # After menuconfig, proceed with the build
        print("[INFO] Starting the kernel build...")
        subprocess.run(["make", "-j$(nproc)"], shell=True, cwd=kernel_dir, check=True)
        print("[SUCCESS] Build completed successfully.")
    except subprocess.CalledProcessError:
        print("[ERROR] Configuration or build failed.")
        sys.exit(1)

# Function to create output directory and package the kernel
def package_kernel(kernel_dir, anykernel_dir):
    try:
        # Copy Image.gz-dtb to AnyKernel directory
        boot_dir = os.path.join(kernel_dir, "arch/arm64/boot")
        image_file = os.path.join(boot_dir, "Image.gz-dtb")
        
        if os.path.exists(image_file):
            print(f"[INFO] Moving {image_file} to AnyKernel directory...")
            shutil.copy(image_file, anykernel_dir)
            
            # Create a zip file in the home directory
            zip_filename = "nethunter-j8-kernel.zip"
            home_directory = os.path.expanduser("~")
            zip_path = os.path.join(home_directory, zip_filename)

            # Zip the AnyKernel directory
            print(f"[INFO] Zipping contents of AnyKernel directory to {zip_path}...")
            subprocess.run(["zip", "-r", zip_path, "."], cwd=anykernel_dir, check=True)

            print(f"[SUCCESS] Kernel packaged successfully as {zip_filename} in the home directory.")
        else:
            print("[ERROR] Image.gz-dtb not found, compilation might have failed.")
    except Exception as e:
        print(f"[ERROR] Failed to package the kernel: {str(e)}")
        sys.exit(1)

# Main function
def main():
    toolchain_dir = "aarch64-linux-android-4.9-toolchain"
    repo_url = "https://github.com/Adrilaw/aarch64-linux-android-4.9-toolchain"
    patches_dir = "patches"  # Directory containing the patches
    kernel_dir = os.getcwd()  # Assuming the script is run from the kernel source directory
    anykernel_dir = os.path.join(kernel_dir, "AnyKernel3")

    # Check and download toolchain if needed
    if not check_toolchain(toolchain_dir):
        download_toolchain(repo_url, toolchain_dir)

    # Set environment variables
    setup_env_variables(toolchain_dir)

    # Apply patches from the patches directory
    apply_patches(patches_dir, kernel_dir)

    # Configure the kernel and build it
    configure_and_build_kernel(kernel_dir)

    # Package the kernel into AnyKernel3 and zip it
    package_kernel(kernel_dir, anykernel_dir)

if __name__ == "__main__":
    main()
