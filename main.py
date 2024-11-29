from InquirerPy import inquirer
import dropbox.exceptions

from dbx_integration import upload_file, dropbox
from ipa_editor import replace_pck
from gh_integration import create_and_clone_and_change_and_push_and_build

import shutil
import os
import dotenv


dotenv.load_dotenv()
IPA = os.getenv("IPA")


def edit_ipa() -> None:
    invalid: bool = False

    while True:
        if not IPA or invalid:
            ipa_path = inquirer.text("Enter path to IPA file to edit:").execute()
        else:
            ipa_path = IPA

        # Check if files exist
        if os.path.exists(ipa_path) and os.path.exists(f"{ipa_path[0:-4]}.pck"):
            break
        else:
            print(
                f"Invalid files! Either '{
                    ipa_path[0:-4]}.pck' and/or {ipa_path} doesn't/don't exist!"
                f"{"\nYour IPA entry in '.env' is faulty!" if IPA and not invalid else ""}"
            )
            invalid = True

    print("Valid files! Replacing PCK file with new one! This may take a minute...")
    replace_pck(ipa_path)
    print("Success!")


def create_new_ipa() -> str:
    print(
        "If you ran this before, delete the folder that this project created on Dropbox!"
    )
    print("Make sure you have enough DropBox space! Otherwise, exit now.")

    while True:
        path = inquirer.text(message="Enter path to folder of XCodeProject:").execute()
        try:
            print("Zipping your project...")
            shutil.make_archive("xcodeproject", "zip", path)
            print("Zipped! Now uploading to Dropbox. THIS MAY TAKE A LONG TIME!!!")

            link = upload_file("tempxcodeproject.zip", "/xcodeproject.zip")
            link = link[0:-1] + "1"
            break
        except FileNotFoundError:
            print("The folder wasn't found.")
            continue
        except dropbox.exceptions.ApiError:
            print(
                "There was an API error. Perhaps try deleting the previous upload from dropbox?"
            )
            quit()

    os.remove("tempxcodeproject.zip")
    print(
        "Success!! Make sure to delete the file once you're done, or else this script will error later!",
        link,
    )
    return link

print("WARNING!!!!!!!\nMAKE SURE YOU ARE RUNNING THIS IN A WORKING DIRECTORY THAT EITHER THE SCRIPT DIRECTORY, OR AN EMPTY DIRECTORY. THANK YOU!!! NOTE TO SELF: REWRITE SO THAT THIS WARNING DOESN'T HAVE TO BE HERE.")
mode = inquirer.select(
    message="Pick a mode",
    choices=["Edit IPA", "Create new IPA"],
).execute()


if mode == "Edit IPA":
    edit_ipa()
    quit()
elif mode == "Create new IPA":
    link = create_new_ipa()

    confirmation = inquirer.confirm("Do you want to continue to uploading to GitHub? If no, quit.", default=True).execute()
    if not confirmation:
        print("Quitting! You can manually build it later on your GitHub repo.")
        quit()
    
    print("Proceeding to the GitHub step!")

    if IPA:
        create_and_clone_and_change_and_push_and_build(link, IPA[0:-4])
    else:
        proj_name = inquirer.text("What's the name of the project?").execute()
        create_and_clone_and_change_and_push_and_build(link, proj_name)
else:
    print("Invalid choice!")
