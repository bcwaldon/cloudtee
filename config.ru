require './service/app'

set :public_folder, "./service/public"
run Sinatra::Application
