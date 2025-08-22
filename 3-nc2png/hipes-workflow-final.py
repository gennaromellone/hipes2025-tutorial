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

    taskB = DagonTask(TaskType.DOCKER, "B", ' \
                    /opt/globo/globone-glowpp/pyglobo/pyglobo-tool.py docker-rainbow --compile --clean -x 2 -y 3 --date 2021-11-17 > compile.out; \
                    chmod +x /opt/globo/globone-glowpp/pyglobo/jobs/run_docker-rainbow_amip_KM312L70.job; \
                    sbatch --wrap="/opt/globo/globone-glowpp/pyglobo/jobs/run_docker-rainbow_amip_KM312L70.job" --wait; \
                    cp /opt/globo/globone-glowpp/runtime/docker-rainbow_KM312L70/GLOBONE_atm_6hrs_2021.nc output.nc'
                    , image="globo")

    taskC = DagonTask(TaskType.DOCKER, "C", 
                      "/app/convert.py --in workflow:///B/output.nc --out result.png ",
                       image="convert-png")

    # add tasks to the workflow
    workflow.add_task(taskA)
    workflow.add_task(taskB)
    workflow.add_task(taskC)

    workflow.make_dependencies()

    # run the workflow
    workflow.run()
