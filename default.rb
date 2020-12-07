#
# Cookbook:: awsasmtest
# Recipe:: default
#
# Copyright:: 2020, The Authors, All Rights Reserved.
#include_recipe "chef-vault"
#vault = chef_vault_item(:chefsecrets, "awschefsecretsmanager")
#aws_access_key = vault["AKIATES3F2LP2NXXM37T"]
#aws_secret_key = vault["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"]


require 'aws-sdk'
require 'json'

client = Aws::SecretsManager::Client.new(region: 'ap-south-1')
#access_key_id: 'AKIATES3F2LP2NXXM37T', secret_access_key: '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')
resp = client.get_secret_value({secret_id: '/app/dev/serviceid'})
password = JSON.parse(resp.secret_string)

# DO NOT DO THIS. JUST SHORTCUTTING TO MAKE SURE THINGS WORK
file '/tmp/output' do
  content "#{password['pasword']}"
  mode '0755'
end