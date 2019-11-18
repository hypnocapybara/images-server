# Python images server
Images converting and storing service. Allow to crop,
resize, rotate images on-fly. 

Has modular architecture with different storage and caches available.
 
Still WIP, but the core already works.

Has 2 URLs:

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
    
___
TODO-list:

- [x] Make core - upload, view, basic transforms
- [ ] Implement filesystem cache
- [ ] Dockerize it!
- [ ] New URL for images from external sources
- [ ] Redis, (memcached?) caches
- [ ] Environment setup: choose cache, storage, disable upload, etc...
- [ ] Smart crop

Optional:
- [ ] Images filters
