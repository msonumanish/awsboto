#
# Cookbook:: myhaproxy
# Recipe:: default
#
# Copyright:: 2021, The Authors, All Rights Reserved.
# frozen_string_literal: true
apt_update

haproxy_install 'package'


# Checking the seach pattern
# search
web_server_array =[]

all_web_servers = search(:node,"role:web AND chef_environment:#{node.chef_environment}",

        filter_result: {
            'name' => ['name'],
            'ip'   => ['ipaddress'],
            'hostname' =>['hostname']

        }
)

all_web_servers.each do |webServer|
  puts webServer['name']
  puts webServer['ip']
  puts webServer['hostname']
  server = "#{webServer['hostname']} #{webServer['ip']}:80 maxconn 32"
  web_server_array.push(server)

  puts node[:loadbalancer][:nodename]

  p node
end



haproxy_frontend 'http-in' do
  bind '*:80'
  default_backend 'servers'
end


haproxy_backend 'servers' do
   server web_server_array
  # [
  #     'web2 192.168.10.44:80 maxconn 32',
  #     'web1 192.168.10.43:80 maxconn 32'
  #   ]

    #notifies :reload , 'haproxy_service[haproxy]' , :immediately
end

haproxy_service 'haproxy' do
    subscribes :reload ,'template[/etc/haproxy/haproxy.cfg]' , :immediately
end