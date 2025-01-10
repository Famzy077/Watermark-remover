# from fastapi import FastAPI, UploadFile, File
# from fastapi.responses import JSONResponse

# app = FastAPI()

# @app.post("/remove-watermark")
# async def remove_watermark(image: UploadFile = File(...)):
#     # Your code to remove watermark from the image goes here
#     return JSONResponse({"message": "Watermark removed successfully!"})
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

@csrf_exempt  # Temporarily disable CSRF for development
def remove_watermark_api(request):
    if request.method == 'POST':
        image_file = request.FILES['image']  # Get the uploaded image
        
        # Convert uploaded image to OpenCV format
        img = np.array(Image.open(image_file))

        # Create a mask for the watermark (For demo purposes, a simple mask)
        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        mask[50:150, 100:200] = 255  # Define the area with the watermark

        # Perform inpainting (remove watermark)
        inpainted_img = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)

        # Convert back to PIL and send as response
        inpainted_pil = Image.fromarray(inpainted_img)
        buffer = BytesIO()
        inpainted_pil.save(buffer, format='JPEG')
        buffer.seek(0)

        return JsonResponse({'message': 'Watermark removed successfully!'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
