import autogen

config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST.json")

llm_config = {
    "cache_seed": 43,
    "temperature": 0,
    "config_list": config_list,
    "timeout": 120,
}

user_proxy = autogen.UserProxyAgent(
    name="Admin",
    system_message=(
        "A human admin overseeing the workflow. "
        "Review plans, execution steps, and final outputs before approval."
    ),
    code_execution_config={"work_dir": "code", "use_docker": False},
    human_input_mode="NEVER",
)

planner = autogen.AssistantAgent(
    name="Planner",
    system_message=(
        "Planner. Suggest a structured plan to execute the task efficiently. "
        "Wait for Admin approval before proceeding. "
        "Ensure clear role assignment: Engineer fetches and processes data, Scientist categorizes papers. "
        "Format the plan in an easy-to-follow manner."
    ),
    llm_config=llm_config,
)

scientist = autogen.AssistantAgent(
    name="Scientist",
    system_message=(
        "Scientist. Analyze the abstracts of fetched papers and categorize them into different domains. "
        "Provide a structured classification without writing code."
    ),
    llm_config=llm_config,
)

engineer = autogen.AssistantAgent(
    name="Engineer",
    system_message=(
        "Engineer. Fetch research papers from arXiv using a Python script. "
        "Process the data and store it in a Markdown table. "
        "Wrap code in code blocks, specifying script type and filename for execution."
    ),
    llm_config=llm_config,
)

critic = autogen.AssistantAgent(
    name="Critic",
    system_message=(
        "Critic. Review the plan, claims, and output from all agents. "
        "Ensure that sources (like arXiv URLs) are included. "
        "Verify correctness of Markdown formatting, domain classification, and fetched data integrity."
    ),
    llm_config=llm_config,
)

group_chat = autogen.GroupChat(
    agents=[user_proxy, planner, engineer, scientist, critic], messages=[], max_round=12
)

manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=llm_config)


user_proxy.initiate_chat(
    manager,
    message=(
        "Trend Analysis of AI Research in Finance Over the Last Year"
    ),
)
