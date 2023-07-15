## API Specification - Image Classification

This API provides functionality for image classification using a pre-trained deep learning model. It accepts image files as input and returns the top predicted classes along with their scores.

### Image Classification

**Endpoint:** `/image/classification`

**Method:** `POST`

**Request Body:**

The request body should contain a JSON object with the following fields:

- `image_paths` (List[str]): A list of paths to image files for classification.

Example Request Body:

```json
{
  "image_paths": [
    "/path/to/image1.jpg",
    "/path/to/image2.jpg",
    "/path/to/image3.jpg"
  ]
}
```

**Response:**

The API will respond with a JSON object containing the classification results for each image. The response structure is as follows:

- `results` (List[dict]): A list of classification results for each image. Each result contains the following fields:
  - `result` (List[dict]): A list of predicted classes for the image. Each class contains the following fields:
    - `name` (str): The name of the predicted class.
    - `score` (float): The confidence score associated with the predicted class.
  - `image` (str, optional): Base64 encoded image representation if available. It can be used to display the image in the API response.

Example Response:

```json
[
    {
      "result": [
        {
          "name": "longberry",
          "score": 98.5
        },
        {
          "name": "premium",
          "score": 1.2
        },
        {
          "name": "peaberry",
          "score": 0.3
        },
        {
          "name": "defect",
          "score": 0.1
        }
      ],
      "image": "base64-encoded-image-data"
    },
    {
      "result": [
        {
          "name": "longberry",
          "score": 95.8
        },
        {
          "name": "defect",
          "score": 3.5
        },
        {
          "name": "premium",
          "score": 0.5
        },
        {
          "name": "peaberry",
          "score": 0.2
        }
      ],
      "image": "base64-encoded-image-data"
    },
    ...
  ]
```

Please note that the `score` field represents the confidence level of the prediction and is expressed as a percentage.

### Error Responses

If an error occurs during the classification process, the API will respond with an error message. The response structure is as follows:

- `error` (str): A descriptive error message explaining the encountered issue.

Example Error Response:

```json
{
  "error": "Failed to open image file."
}
```

### Endpoint URL

The API is accessible at the following URL:

```
https://api.example.com/image/classification
```

Please ensure to replace `api.example.com` with the actual domain of the API.

### Additional Notes

- The API uses a pre-trained deep learning model and requires appropriate model files and dependencies to be available for successful execution.
- The API supports image formats compatible with the `PIL` library, such as JPEG, PNG, etc.
- Make sure to send the requests using the `POST` method.
- The API response is sorted in descending order based on the highest scoring predicted class.
- The maximum number of predicted classes returned for each image is four.

That's it! You can use this API specification as a reference for integrating the image classification functionality into your application.
