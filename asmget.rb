#
# Cookbook:: awsasmtest
# Recipe:: default
#
# Copyright:: 2020, The Authors, All Rights Reserved.
#include_recipe "chef-vault"
#vault = chef_vault_item(:chefsecrets, "awschefsecretsmanager")
#aws_access_key = vault["AKIATES3F2LP2NXXM37T"]
#aws_secret_key = vault["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"]


require 'json'

execute 'get asm value' do
  command "aws secretsmanager get-secret-value --secret-id /app/dev/serviceid --query SecretString --region ap-south-1 --output text>> /tmp/cli.json"
end

ruby_block "get secret value" do
  block do
      file = File.read('/tmp/cli.json')
      data_hash = JSON.parse(file)
      password = data_hash['pasword']
      puts (data_hash)
      puts "This is a test............. #{password}"
      node.run_state['transferred_files']=password

      puts "This is a puts from the top of the default recipe; node info: #{node.run_state['transferred_files']}"
  end
end

puts "Out side chef recipe; node info: #{node.run_state['transferred_files']}"
Chef::Log.warn("You can log node info #{node['foo']} from a recipe using 'Chef::Log'")
  
file '/tmp/password.txt' do
  content lazy {"#{node.run_state['transferred_files']}"}
  mode '0755'
end