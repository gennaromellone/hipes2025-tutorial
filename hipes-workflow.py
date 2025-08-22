from dagon import Workflow
from dagon.task import DagonTask, TaskType

# Check if this is the main
if __name__ == '__main__':    
    # Create the orchestration workflow
    workflow=Workflow("DataFlow-Demo")

    # The task a
    taskA = DagonTask(TaskType.BATCH, "A", "echo 2 > x.txt; echo 3 > y.txt")

    #taskB = DagonTask(TaskType.DOCKER, "B", 'chmod +x pyglobo-tool.py; ./pyglobo-tool.py rainbow --run GLOBISSIMO --date 2021-11-17 -x 2 -y 3; squeue', image="globo")
    taskB = DagonTask(TaskType.DOCKER, "B", ' \
                    /opt/globo/globone-glowpp/pyglobo/pyglobo-tool.py rainbow --compile --clean -x 2 -y 3 --date 2021-11-17 > compile.out; \
                    chmod +x /opt/globo/globone-glowpp/pyglobo/jobs/run_rainbow_amip_KM312L70.job; \
                    sbatch --wrap="/opt/globo/globone-glowpp/pyglobo/jobs/run_rainbow_amip_KM312L70.job"; \
                    sleep 150; \
                    cp /opt/globo/globone-glowpp/runtime/rainbow_KM312L70/GLOBONE_atm_6hrs_2021.nc output.nc \
                    '
    , image="globo")

    taskC = DagonTask(TaskType.DOCKER, "C", "/app/convert.py --in workflow:///B/output.nc --out result.png ",
                       image="convert-png")
    #taskB = DagonTask(TaskType.DOCKER, "B", '/opt/globo/globone-glowpp/pyglobo/pyglobo-tool.py rainbow --run GLOBISSIMO --date 2021-11-17 -x 2 -y 3 >> a.out', image="globo")
    #taskC = DagonTask(TaskType.BATCH, "C", "cat workflow:///B/output.nc > output.nc")
    # The task

    # add tasks to the workflow
    workflow.add_task(taskA)
    workflow.add_task(taskB)
    workflow.add_task(taskC)

    workflow.make_dependencies()

    # run the workflow
    workflow.run()
