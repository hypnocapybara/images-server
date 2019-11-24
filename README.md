# Python images server
Images converting and storing service. Allow to crop,
resize, rotate images on-fly. 

Has modular architecture with different storage and caches available.
 
### Usage
Just use this image in your docker-compose:
```yaml
version: '3'
services:
  web:
    image: hypnocapybara/images-server
    volumes:
      - ./uploads:/app/uploads
    ports:
      - "5000:80"
```

And it goes to 5000 port


### Operations
Has following operations:

1. `POST /upload` with `file` parameter. Will save 
provided file in chosen storage and on success return: 
    ```json
    {
    "hash": "<hash>",
    "status": "success"
    }
    ```
  
2. `GET /image/<hash>` will return saved image.

    Also possible to perform operations pipeline:
    `/image/<hash>/resize/x200/crop/e200x200`
    
3. Crop: `GET /image/<hash>/crop/<gravity><width>x<height>`, ex: `c200x200`

    Possible gravity values: 
     - 'nw' - 'north_west',
     - 'n' - 'north',
     - 'ne' - 'north_east',
     - 'w' - 'west',
     - 'c' - 'center',
     - 'e' - 'east',
     - 'sw' - 'south_west',
     - 's' - 'south',
     - 'se' - 'south_east'
   
4. Resize: `GET /image/<hash>/resize/<geometry>` ex: `200x` 

    Geometry examples:
    - `200x200` - specified size
    - `x100` - height = 100px, width calculated automatically
    - `300x200>` if larger than 300x200, fit within box, preserving aspect ratio

    Other examples at ImageMagic documentation: https://www.imagemagick.org/script/command-line-processing.php#geometry
   
5. Combined: `GET /image/<hash>/resize/400x400/crop/n100x100`
    
6. External images: `GET /external?url=<external_image_url>&operations=<operations>`
    
    Possible `<operations>` are listed above
    
    `<external_image_url>` must contain valid external image
    
    Default cache will be used to store the processed image.
    If you want to update the image (for example, it was
    changed, but URL is just the same), you may add
    `reset_cache=1` GET param to the URL, ex:
    
    `GET /external?url=<external_image_url>&operations=<operations>&reset_cache=1`
    
    But pay attention, that with this param, the image will be 
    always downloaded, that may slow down the request.

___
TODO-list:

- [x] Make core - upload, view, basic transforms
- [x] Implement filesystem cache
- [x] Dockerize it!
- [x] Publish docker image
- [x] New URL for images from external sources
- [ ] Redis, (memcached?) caches
- [ ] Environment setup: choose cache, storage, disable upload, etc...
- [ ] Delete images
- [ ] Tests
- [ ] Smart crop

Optional:
- [ ] Images filters
