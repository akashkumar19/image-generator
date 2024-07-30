## To Run the application

- create a `.env` file same as `.env.example` file.
- Paste the stability AI `api-key` in `.env` file.

> Run the following command in terminal to start the application

```sh
docker compose up
```

- After that visit the `http://localhost:8000/generator/generate/` to test the api.
- Steps to copy the image into the current directory 
```sh
docker cp image_generator:./image_generator/out/A_red_flying_dog_0.png .
docker cp image_generator:./image_generator/out/A_piano_ninja_0.png .
docker cp image_generator:./image_generator/out/A_red_flying_dog_0.png .
```
