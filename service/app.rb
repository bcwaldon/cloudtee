require 'sinatra'

set :public_folder, 'public'

get '/' do
    "<center><img src='/logo.png'/></center>"
end

$pages = {}

get '/:page' do
    page = $pages[params[:page]] || []
    "<pre>#{page.join("\n")}</pre>"
end

post '/:page' do
    $pages[params[:page]] ||= []
    $pages[params[:page]].push request.body.read
    "Success"
end
