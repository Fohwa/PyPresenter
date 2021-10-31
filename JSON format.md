# Brainstorming for Json formatting in PyPresenter

### Should one file be one slide or should be one directory?
- Should only be per slide for now
- could be for complete song e.g. in future

### What info must be stored scalability and ease of use in mind?
- type: slide, song, config, etc. (video, sound, etc.)
- meta data:
    - resolution of slide
    - name
    - number of objects
- objects
    - object
        - mode: text, image, shape
        - coordinates (relative to screen size)
        - size (relative to screen size)
        - for image: location
        - for text: text, size, font, color (rgb), etc. (shadows)
        