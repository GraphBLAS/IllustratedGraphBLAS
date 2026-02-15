from .logos import create_logo_grid, LOGO_FILENAMES
from .matrix_utils import (
    CHAPTER0_MATRIX_DATA,
    CHAPTER3_MATRIX_DATA,
    create_labeled_matrix,
    hide_zero_entries,
    get_non_zero_positions,
    get_zero_positions,
)
from .graph_utils import (
    create_adjacency_digraph,
    create_undirected_graph,
    set_vertex_fill_preserve_label,
    animate_vertex_fill,
)
from .speech import get_speech_service, setup_scene, is_prod_mode
