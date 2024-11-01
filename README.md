# IllustratedGraphBLAS

To start create a virtual environment and install requirements:

```
virtualenv --python=python3 .virt
. .virt/bin/activate
pip install -r requirements.txt
```

To build a scene in a chapter

```
invoke build-scene --chapter Chapter0 --scene Scene0 --quality l
```

To build all scenes in a chapter:

```
invoke build-chapter --chapter Chapter0 --quality l
```

To stich all scenes in a final video

```
invoke stitch-videos --chapter Chapter0 --quality l
```

