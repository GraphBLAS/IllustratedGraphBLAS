# IllustratedGraphBLAS

To start create a virtual environment and install requirements:

```
virtualenv --python=python3 .virt
. .virt/bin/activate
pip install -r requirements.txt
```

Manim quality settings are (l) low, (m) medium, (h), high and can be
passed in the `--quality` argument.

To build a scene in a chapter:

```
invoke build-scene --chapter Chapter0 --scene Scene0 --quality l
```

To build all scenes in a chapter:

```
invoke build-chapter --chapter Chapter0 --quality l
```

To build all chapters:

```
invoke build-all --quality l
```

To stich all scenes in a chapter final video of a given quality:

```
invoke stitch-chapter --chapter Chapter0 --quality l
```

To stich all chapters with a given quality:

```
invoke stitch-all --quality l
```

To render thumbnails:

```
invoke render-thumbnails
```

To clean all media in a chapter:

```
invoke clean-chapter --chapter Chapter0
```

To clean all chapters:

```
invoke clean-all
```

To clean, build, stitch and render all thumbnails:

```
invoke all --quality l
```





