{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      utils,
    }:
    utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };
        ignis = pkgs.stdenv.mkDerivation rec {
          name = "igins";
          pname = "Ignis";
          src = pkgs.fetchFromGitHub {
            owner = "linkfrg";
            repo = "ignis";
            rev = "main";
            sha256 = "zSWkckB2XDJuVbXrvyj/FGbI6AQwnbKRs6RV7y56jH0=";
          };

          gvc = pkgs.fetchFromGitLab {
            domain = "gitlab.gnome.org";
            owner = "GNOME";
            repo = "libgnome-volume-control";
            rev = "5f9768a2eac29c1ed56f1fbb449a77a3523683b6";
            hash = "sha256-gdgTnxzH8BeYQAsvv++Yq/8wHi7ISk2LTBfU8hk12NM=";
          };

          nativeBuildInputs = [
            pkgs.pkg-config
            pkgs.meson
            pkgs.ninja
            pkgs.git
            pkgs.makeWrapper
          ];

          buildInputs = [
            pkgs.glib
            pkgs.gtk4
            pkgs.gtk4-layer-shell
            pkgs.libpulseaudio
            pkgs.python312Packages.pygobject3
            pkgs.python312Packages.pycairo
            pkgs.python312Packages.click
            pkgs.python312Packages.charset-normalizer
            pkgs.gst_all_1.gstreamer
            pkgs.gst_all_1.gst-plugins-base
            pkgs.gst_all_1.gst-plugins-good
            pkgs.gst_all_1.gst-plugins-bad
            pkgs.gst_all_1.gst-plugins-ugly
            pkgs.pipewire
            pkgs.dart-sass
          ];

          patchPhase = ''
            mkdir -p ./subprojects/gvc
            cp -r ${gvc}/* ./subprojects/gvc
            substituteInPlace ignis/utils/sass.py \
              --replace-fail '/bin/sass' '${pkgs.dart-sass}/bin/sass'
          '';

          buildPhase = ''
            cd ..
            meson setup build --prefix=$out --libdir=lib/ignis
            ninja -C build
          '';

          installPhase = ''
            ninja -C build install
            cp -r $src/ignis $out/lib/python3.12/site-packages
          '';

          # nativeBuildInputs = [
          #   pkgs.pkg-config
          #   pkgs.git
          #   pkgs.makeWrapper
          #   pkgs.meson
          # ];
          #
          # buildInputs = [
          #   pkgs.glib
          #   pkgs.gtk4
          #   pkgs.gtk4-layer-shell
          #   pkgs.libpulseaudio
          #   pkgs.python312Packages.pygobject3
          #   pkgs.python312Packages.pycairo
          #   pkgs.python312Packages.click
          #   pkgs.python312Packages.charset-normalizer
          #   pkgs.gst_all_1.gstreamer
          #   pkgs.gst_all_1.gst-plugins-base
          #   pkgs.gst_all_1.gst-plugins-good
          #   pkgs.gst_all_1.gst-plugins-bad
          #   pkgs.gst_all_1.gst-plugins-ugly
          #   pkgs.pipewire
          #   pkgs.dart-sass
          # ];
          #
          # unpackPhase = ''
          #   	    cd $src
          # '';
          #
          # configurePhase = '''';
          #
          # installPhase = ''
          #   mkdir -p $out/lib/python3.12/site-packages
          #   cp -r $src/ignis $out/lib/python3.12/site-packages
          # '';
        };
      in
      {
        devShell =
          with pkgs;
          mkShell {
            buildInputs = [
              ignis
              pkgs.glib
              pkgs.gtk4
              pkgs.gtk4-layer-shell
              pkgs.libpulseaudio
              pkgs.python312Packages.pygobject3
              pkgs.python312Packages.pycairo
              pkgs.python312Packages.click
              pkgs.python312Packages.charset-normalizer
              pkgs.python312Packages.requests
              pkgs.python312Packages.setuptools
              pkgs.python312Packages.loguru
              pkgs.gst_all_1.gstreamer
              pkgs.gst_all_1.gst-plugins-base
              pkgs.gst_all_1.gst-plugins-good
              pkgs.gst_all_1.gst-plugins-bad
              pkgs.gst_all_1.gst-plugins-ugly
              pkgs.pipewire
              pkgs.dart-sass
            ];
            PYTHONPATH = "${ignis}/lib/python3.12/site-packages";
            LD_LIBRARY_PATH = "${pkgs.gtk4-layer-shell}/lib";
            shellHook = ''
              exec fish
            '';
          };
      }
    );
}
