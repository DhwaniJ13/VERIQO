# importing required tools for file upload
from fastapi import APIRouter, UploadFile, File, HTTPException
# path for path of file & folder, shutil to copy data
from pathlib import Path
import shutil
import uuid

# creating a separate router for upload-related APIs which is separated from main one
router = APIRouter()

# location where uploaded documents will be stored i.e data->uploads
UPLOAD_DIR = Path("data/uploads")

# create the uploads folder if it doesn't exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# allowed document formats for uploading docs
# different formats will later be processed using different extraction methods
ALLOWED_EXTENSIONS = {".pdf",".png",".jpg",".jpeg",".doc",".docx",".csv",".txt",".xlsx"}

@router.post("/upload")  # so that FastAPI knows which function to execute

async def upload_document(
    file: UploadFile = File(...)
):  # creates function named upload_document

    # checking whether a file was actually uploaded
    # if no file is provided, we stop the request & print error msg

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file was uploaded."
        )


    # getting the file extension like PDF is same as pdf & lower() makes it same

    file_extension = Path(file.filename).suffix.lower()


    # if extenion not supported then display error message with status code 400

    if file_extension not in ALLOWED_EXTENSIONS:

        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Please upload PDF, PNG, JPG, JPEG, DOC, DOCX, CSV, TXT or XLSX."
        )

    # creating a unique internal filename instad or orginial name for security an davoid duplicacy
    unique_filename = f"{uuid.uuid4().hex}{file_extension}"

    # creating the complete path where the file will be saved
    file_path = UPLOAD_DIR / unique_filename

    # limiting the maximum uploaded document size for security
    MAX_FILE_SIZE = 10 * 1024 * 1024

    # variable used to keep track of how many bytes have been uploaded
    total_size = 0


    # trying to safely save the uploaded document
    try:
        with open(file_path, "wb") as buffer:#as pdf arent ordinary text file so wb for binary

            while True:
                chunk = await file.read(1024 * 1024) # # reading 1 MB at a time so avoid consuiming more memory

                if not chunk:
                    break   ## stop loop if no data

                # adding the size of the current chunk to the total uploaded file size
                total_size += len(chunk)

                # checking whether the file has crossed the 10 MB limit
                if total_size > MAX_FILE_SIZE:

                    # deleting the partially uploaded file so oversized doc is not left on server
                    file_path.unlink(missing_ok=True)

                    raise HTTPException(
                        status_code=413,
                        detail="File is too large. Maximum allowed size is 10 MB."
                    ) # sending HTTP 413 for Too Large file

                # writing the current chunk to the destination file
                buffer.write(chunk)


    # if we intentionally raised HTTPException above then pass same error to the user

    except HTTPException:
        raise

    # handling unexpected errors while saving the document
    except Exception:
        # if something goes wrong, delete any partially saved file
        file_path.unlink(missing_ok=True)

        # sending a server error response
        raise HTTPException(
            status_code=500,
            detail="Could not securely save the uploaded document."
        )

    # this runs whether the upload succeeds or fails
    # it closes the uploaded file and releases resources

    finally:
        await file.close()

    # sending a response back to the user-we return org. filename for display

    return {
        "message": "Document uploaded successfully",
        "filename": file.filename,
        "document_id": unique_filename,
        "status": "uploaded"
    }