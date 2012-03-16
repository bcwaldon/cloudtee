require 'sinatra'

get '/' do
    "<center><img src='/logo.png'/><br><pre>pip install cloudtee\ndpkg -l | cloudtee packages\nvisit <a href='/packages'>http://cloudtee.me/packages</a></pre></center>"
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
