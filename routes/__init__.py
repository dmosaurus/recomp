from .dashboard  import bp as dashboard_bp
from .program    import bp as program_bp
from .log        import bp as log_bp
from .history    import bp as history_bp
from .progress   import bp as progress_bp
from .nutrition  import bp as nutrition_bp
from .body_scan  import bp as body_scan_bp

all_blueprints = [dashboard_bp, program_bp, log_bp, history_bp, progress_bp, nutrition_bp, body_scan_bp]
