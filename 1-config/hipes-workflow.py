from dagon import Workflow
from dagon.task import DagonTask, TaskType

# Check if this is the main
if __name__ == '__main__':    
    # Create the orchestration workflow
    workflow=Workflow("HiPES2025-Workflow-Demo", config_file="../dagon.ini")

    # The task a
    taskA = DagonTask(TaskType.BATCH, "A", 
                      "echo 2 > x.txt; echo 3 > y.txt"
                      )

    # add tasks to the workflow
    workflow.add_task(taskA)

    workflow.make_dependencies()

    # run the workflow
    workflow.run()
