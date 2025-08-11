import json
import pathlib
import os

html_template = """<!DOCTYPE html>
<html>
  <head>
    <meta
      name="go-import"
      content="{import_prefix} git https://github.com/{owner}/{repo_name}.git"
    />
    <meta charset="utf-8" />
    <meta
      http-equiv="refresh"
      content="0; url=https://pkg.go.dev/{import_prefix}"
    />
  </head>
  <body>
    Redirecting to
    <a href="https://pkg.go.dev/{import_prefix}"
      >https://pkg.go.dev/{import_prefix}</a
    >...
  </body>
</html>
"""


def exit_with_error(msg: str):
    print(msg)
    exit(1)


def make_html(import_prefix: str, owner: str, repo_name: str, dir: str):
    dir_path = pathlib.Path(repo_name) / dir
    html_file_path = dir_path / "index.html"

    os.makedirs(dir_path, exist_ok=True)

    with open(html_file_path, "w") as f:
        f.write(
            html_template.format(
                import_prefix=import_prefix,
                owner=owner,
                repo_name=repo_name,
            )
        )


def main():
    payload = json.loads(input())

    try:
        owner: str = payload["Owner"]
        repo_name: str = payload["RepoName"]

        go_mod_info = payload["GoModInfo"]

        module = go_mod_info["Module"]
        imports: list[str] = go_mod_info["Imports"]

        mod_path: str = module["Path"]
    except KeyError as e:
        exit_with_error(f"invalid payload: {e}")

    import_paths: list[str] = [mod_path] + [
        imp for imp in imports if imp.startswith(mod_path)
    ]

    import_suffix = [imp.removeprefix(mod_path) for imp in import_paths]

    for suffix in import_suffix:
        make_html(mod_path, owner, repo_name, suffix)


if __name__ == "__main__":
    main()
