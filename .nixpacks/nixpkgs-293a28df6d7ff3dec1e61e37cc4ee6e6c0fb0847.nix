{ }:

let pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/293a28df6d7ff3dec1e61e37cc4ee6e6c0fb0847.tar.gz") { overlays = [  ]; };
in with pkgs;
  let
    APPEND_LIBRARY_PATH = "${lib.makeLibraryPath [ stdenv.cc.cc.lib zlib ] }";
    myLibraries = writeText "libraries" ''
      export LD_LIBRARY_PATH="${APPEND_LIBRARY_PATH}:$LD_LIBRARY_PATH"
      
    '';
  in
    buildEnv {
      name = "293a28df6d7ff3dec1e61e37cc4ee6e6c0fb0847-env";
      paths = [
        (runCommand "293a28df6d7ff3dec1e61e37cc4ee6e6c0fb0847-env" { } ''
          mkdir -p $out/etc/profile.d
          cp ${myLibraries} $out/etc/profile.d/293a28df6d7ff3dec1e61e37cc4ee6e6c0fb0847-env.sh
        '')
        gcc python38
      ];
    }
