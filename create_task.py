import subprocess
import os

# Set the API key in the environment
env = os.environ.copy()
env['NOTION_API_KEY'] = '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'

# Create scheduled task using schtasks via python
command = '''
schtasks /create /tn "GitHub Stars Sync" /tr "python C:\\GitHub\\claude-assist\\github_stars_to_notion.py" /sc daily /st 09:00 /f
'''

result = subprocess.run(['schtasks', '/create', '/tn', 'GitHub Stars Sync',
                        '/tr', 'python C:\\GitHub\\claude-assist\\github_stars_to_notion.py',
                        '/sc', 'daily', '/st', '09:00', '/f'],
                       capture_output=True, text=True, shell=True)

print(result.stdout)
print(result.stderr)

if 'SUCCESS' in result.stdout or result.returncode == 0:
    print("\nScheduled task created!")
    print("Run 'schtasks /query | findstr Stars' to verify")
else:
    print("\nTask creation had issues. Try running as Administrator.")
