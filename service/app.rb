require 'sinatra'

get '/' do
    "<center><img src='/logo.png'/><br><pre>1. pip install cloudtee\n2. dpkg -l | cloudtee packages\n3. visit <a href='/packages'>http://cloudtee.me/packages</a></pre></center>"
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
