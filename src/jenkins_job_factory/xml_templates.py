import html
import uuid


def folder_xml(folder_name: str) -> str:
    safe_name = html.escape(folder_name)

    return f"""<?xml version='1.1' encoding='UTF-8'?>
<com.cloudbees.hudson.plugins.folder.Folder>
  <description>{safe_name}</description>
  <displayName>{safe_name}</displayName>
  <properties>
    <com.datapipe.jenkins.vault.configuration.FolderVaultConfiguration>
      <configuration>
        <failIfNotFound>true</failIfNotFound>
        <skipSslVerification>false</skipSslVerification>
        <disableChildPoliciesOverride>false</disableChildPoliciesOverride>
        <timeout>60</timeout>
      </configuration>
    </com.datapipe.jenkins.vault.configuration.FolderVaultConfiguration>
    <org.jenkinsci.plugins.pipeline.maven.MavenConfigFolderOverrideProperty>
      <settings class="jenkins.mvn.DefaultSettingsProvider"/>
      <globalSettings class="jenkins.mvn.DefaultGlobalSettingsProvider"/>
      <override>false</override>
    </org.jenkinsci.plugins.pipeline.maven.MavenConfigFolderOverrideProperty>
  </properties>
  <folderViews class="com.cloudbees.hudson.plugins.folder.views.DefaultFolderViewHolder">
    <views>
      <hudson.model.AllView>
        <owner class="com.cloudbees.hudson.plugins.folder.Folder" reference="../../../.."/>
        <name>All</name>
        <filterExecutors>false</filterExecutors>
        <filterQueue>false</filterQueue>
        <properties class="hudson.model.View$PropertyList"/>
      </hudson.model.AllView>
    </views>
    <tabBar class="hudson.views.DefaultViewsTabBar"/>
  </folderViews>
  <healthMetrics/>
  <icon class="com.cloudbees.hudson.plugins.folder.icons.StockFolderIcon"/>
</com.cloudbees.hudson.plugins.folder.Folder>
"""


def multibranch_xml(
    job_name: str,
    repo_url: str,
    credentials_id: str,
    script_id: str,
    branch_regex: str,
) -> str:
    source_id = str(uuid.uuid4())

    return f"""<?xml version='1.1' encoding='UTF-8'?>
<org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject plugin="workflow-multibranch">
  <actions/>
  <description>{html.escape(job_name)}</description>
  <displayName>{html.escape(job_name)}</displayName>

  <properties>
    <org.jenkinsci.plugins.configfiles.folder.FolderConfigFileProperty>
      <configs class="sorted-set">
        <comparator class="org.jenkinsci.plugins.configfiles.ConfigByIdComparator"/>
      </configs>
    </org.jenkinsci.plugins.configfiles.folder.FolderConfigFileProperty>

    <org.jenkinsci.plugins.docker.workflow.declarative.FolderConfig>
      <dockerLabel></dockerLabel>
      <registry/>
    </org.jenkinsci.plugins.docker.workflow.declarative.FolderConfig>

    <com.datapipe.jenkins.vault.configuration.FolderVaultConfiguration>
      <configuration>
        <failIfNotFound>true</failIfNotFound>
        <skipSslVerification>false</skipSslVerification>
        <disableChildPoliciesOverride>false</disableChildPoliciesOverride>
        <timeout>60</timeout>
      </configuration>
    </com.datapipe.jenkins.vault.configuration.FolderVaultConfiguration>

    <org.jenkinsci.plugins.pipeline.maven.MavenConfigFolderOverrideProperty>
      <settings class="jenkins.mvn.DefaultSettingsProvider"/>
      <globalSettings class="jenkins.mvn.DefaultGlobalSettingsProvider"/>
      <override>false</override>
    </org.jenkinsci.plugins.pipeline.maven.MavenConfigFolderOverrideProperty>
  </properties>

  <folderViews class="jenkins.branch.MultiBranchProjectViewHolder">
    <owner class="org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject" reference="../.."/>
  </folderViews>

  <healthMetrics/>

  <icon class="jenkins.branch.MetadataActionFolderIcon">
    <owner class="org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject" reference="../.."/>
  </icon>

  <orphanedItemStrategy class="com.cloudbees.hudson.plugins.folder.computed.DefaultOrphanedItemStrategy">
    <pruneDeadBranches>true</pruneDeadBranches>
    <daysToKeep>-1</daysToKeep>
    <numToKeep>-1</numToKeep>
    <abortBuilds>false</abortBuilds>
  </orphanedItemStrategy>

  <triggers/>
  <disabled>false</disabled>

  <sources class="jenkins.branch.MultiBranchProject$BranchSourceList">
    <data>
      <jenkins.branch.BranchSource>
        <source class="jenkins.plugins.git.GitSCMSource">
          <id>{source_id}</id>
          <remote>{html.escape(repo_url)}</remote>
          <credentialsId>{html.escape(credentials_id)}</credentialsId>
          <traits>
            <jenkins.plugins.git.traits.BranchDiscoveryTrait/>
            <jenkins.scm.impl.trait.RegexSCMHeadFilterTrait>
              <regex>{html.escape(branch_regex)}</regex>
            </jenkins.scm.impl.trait.RegexSCMHeadFilterTrait>
          </traits>
        </source>

        <strategy class="jenkins.branch.DefaultBranchPropertyStrategy">
          <properties class="empty-list"/>
        </strategy>
      </jenkins.branch.BranchSource>
    </data>

    <owner class="org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject" reference="../.."/>
  </sources>

  <factory class="org.jenkinsci.plugins.pipeline.multibranch.defaults.PipelineBranchDefaultsProjectFactory">
    <owner class="org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject" reference="../.."/>
    <scriptId>{html.escape(script_id)}</scriptId>
    <useSandbox>false</useSandbox>
  </factory>
</org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject>
"""