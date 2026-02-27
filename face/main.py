import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.face import FaceClient
from azure.ai.vision.face.models import (
    FaceAttributeTypeDetection03,
    FaceDetectionModel,
    FaceRecognitionModel,
)

load_dotenv()

KEY = os.environ["FACE_APIKEY"]
ENDPOINT = os.environ["FACE_ENDPOINT"]

# Sample images to detect faces in
test_images = [
    "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/Family1-Mom1.jpg",
    "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/Family1-Dad1.jpg",
    "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/Face/images/identification1.jpg",
]

with FaceClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY)) as face_client:
    for image_url in test_images:
        print(f"\nDetecting faces in: {image_url.split('/')[-1]}")
        print("-" * 60)

        detected_faces = face_client.detect_from_url(
            url=image_url,
            detection_model=FaceDetectionModel.DETECTION03,
            recognition_model=FaceRecognitionModel.RECOGNITION04,
            return_face_id=False,
            return_face_attributes=[
                FaceAttributeTypeDetection03.HEAD_POSE,
                FaceAttributeTypeDetection03.MASK,
                FaceAttributeTypeDetection03.BLUR,
            ],
            return_face_landmarks=True,
        )

        if not detected_faces:
            print("  No faces detected.")
            continue

        print(f"  {len(detected_faces)} face(s) detected:\n")
        for i, face in enumerate(detected_faces, 1):
            rect = face.face_rectangle
            print(f"  Face #{i}")
            print(f"    Bounding box: top={rect.top}, left={rect.left}, "
                  f"width={rect.width}, height={rect.height}")

            attrs = face.face_attributes
            if attrs:
                if attrs.head_pose:
                    hp = attrs.head_pose
                    print(f"    Head pose: yaw={hp.yaw:.1f}, pitch={hp.pitch:.1f}, roll={hp.roll:.1f}")
                if attrs.mask:
                    print(f"    Mask: type={attrs.mask.type}, nose_and_mouth_covered={attrs.mask.nose_and_mouth_covered}")
                if attrs.blur:
                    print(f"    Blur: level={attrs.blur.blur_level}, value={attrs.blur.value:.2f}")
    print("\nDone.")