# LAMMPS Docset

Build a docset from a LAMMPS archive for offline API documentation browsers such as [Dash](https://kapeli.com/dash) and [Zeal](https://zealdocs.org/).

## How to ...

### Use GitHub Actions to build the docset

- Go to [workflow dispatch][1].
- Click "Run workflow" button.
- Set the URL for LAMMPS archive, such as `https://download.lammps.org/tars/lammps-23Jun2022.tar.gz`,
  if you leave it empty, it will use the latest LAMMPS build.
- Click the green "Run workflow" button.
- Wait for the workflow to finish.
- Download the payload from the successful workflow run.

[1]: https://github.com/chazeon/lammps-docset/actions/workflows/build.yml

### Build locally

- Install Doxygen
- Install build requirements
  ```sh
  pip install -r requirements.txt
  ```
- Use the [Makefile](./Makefile) to build documents, it will download the archive automatically.
  ```sh
  make docset
  ```

## Licence

Licenced under the [MIT licence](./LICENSE).
