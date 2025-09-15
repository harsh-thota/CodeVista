from __future__ import annotations
from typing import TypedDict, List, Dict
from pathlib import Path
from platformdirs import user_config_dir
from datetime import datetime
import json

APP_NAME = "code-vista"

# FIXME: these data types are soo redundant, need a better way do this
class FileHistory(TypedDict):
    file: str
    last_commit_date: str

class TaskItem(TypedDict):
    comment: str
    file: str
    line: int

class DependencyNode(TypedDict):
    id: str

class DependencyLink(TypedDict):
    source: str
    target: str

class LargestFile(TypedDict):
    path: str
    size_bytes: str

class DependencyGraph(TypedDict):
    nodes: List[DependencyNode]
    links: List[DependencyLink]

class ProjectSummary(TypedDict):
    total_files: int
    total_lines_of_code: int
    languages: Dict[str, int]


class ProjAnalysis:
    project_name: str
    path: str
    last_analyzed: str
    summary: ProjectSummary
    largest_files: List[LargestFile]
    task_list: List[TaskItem]
    dependency_graph: DependencyGraph
    git_history: List[FileHistory]

class AppStorage(TypedDict):
    version: int
    projects_folder: str
    projects: List[ProjAnalysis]


class Storage(TypedDict):
    def __init__(self, app_name: str = APP_NAME):
        self.storage_dir = Path(user_config_dir(APP_NAME))
        self.file_path = self.get_storage_path()
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def get_storage_path(self) -> Path:
        return self.storage_dir / "storage.json"
    
    def load_data(self) -> AppStorage:
        if not self.file_path.exists():
            default_storage: AppStorage = {
                "version": 1,
                "projects_folder": "",
                "projects": []
            }
            with open(self.file_path, "w") as f:
                json.dump(default_storage, f, indent=2)
            return default_storage
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Heads up! Couldn't load data from {self.file_path}: {e}")
            return {
                "version": 1,
                "projects_folder": "",
                "projects": [],
            }
    
    def save_data(self, data: AppStorage) -> None:
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"ouldn't save data to {self.file_path}: {e}")

    def update_project(self, new_analysis: ProjAnalysis) -> None:
        app_data = self.load_data()
        updated = False
        for i, project in enumerate(app_data["projects"]):
            if project["path"] == new_analysis["path"]:
                app_data["projects"][i] = new_analysis
                updated = True
                break
        if not updated:
            app_data["storage"].append(new_analysis)

        self.save_data(app_data)
